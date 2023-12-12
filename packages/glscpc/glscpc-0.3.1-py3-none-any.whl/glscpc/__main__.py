import glob
import itertools
import logging
import os.path
import shlex
import shutil
import traceback
from typing import IO, Any, BinaryIO, Optional, Tuple, Union

import click
from click.exceptions import Exit

from glscpc import ASCII_ONLY, ASCII_REPLACE_TABLE, Checker, IncludeMode

from ._version import __version__

VERBOSE_OPTIONS = [logging.WARNING, logging.INFO, logging.DEBUG]
# Default command: Take from stdin, use POSIX shell, format output as JSON1
DEFAULT_COMMAND = ["shellcheck", "-", "--shell=sh", "--format=json1"]
MINIMUM_WRAP = 50
DEFAULT_WRAP = 160
QTEAL = click.style("Q", fg="cyan") + click.style("teal", fg="bright_black")
LOGO = f"""
┏━╸╻  ┏━┓┏━╸┏━┓┏━╸  {QTEAL}
┃╺┓┃  ┗━┓┃  ┣━┛┃    {click.style('fixing systems, not people', fg='bright_black')}
┗━┛┗━╸┗━┛┗━╸╹  ┗━╸  v{__version__}
""".strip()
# Padding required to make sure click keeps the logo intact.
HELP = """
Check your .gitlab-ci.yml scripts with ShellCheck.

This project does not lint the rest of the file(s) and assumes they are well-formed and valid. Please use another checker for that purpose.

Any other arguments passed will be forwarded to shellcheck as additional arguments. The full command is printed when DEBUG logging is
enabled.

It is recommended to pass any arguments to ShellCheck after using -- to end option parsing for glscpc, to preserve forward compatability
with new options.
"""


class GlobFileType(click.File):
    """
    Click file type argument that resolves globs.
    The output is a tuple of files!
    """

    def convert(
        self, value: Union[str, "os.PathLike[str]", IO[Any]], param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Tuple[IO[Any]]:
        # If nothing matches the glob, pretend, so the underlying click function can print a nice error.
        value = glob.glob(value) or [value]
        return tuple(super(GlobFileType, self).convert(x, param, ctx) for x in value)


def transform_return(e: Any) -> str:
    """
    Process the returned (or yielded) values from process_file into strings for output to user.
    This also deals with "ASCII only" mode.
    """
    if isinstance(e, str):
        if ASCII_ONLY:
            return click.unstyle(e).translate(ASCII_REPLACE_TABLE)
        return e
    if isinstance(e, Exception):
        return "".join(traceback.format_exception_only(e))
    return repr(e)


@click.command(
    context_settings={
        # Help is still wrapped to terminal width, but ignore the 80 char default max.
        "max_content_width": 1000,
        # All unknown options are passed to shellcheck later
        "ignore_unknown_options": True,
    },
    # \b selectively disables all re-wrapping on the next paragraph, which makes the logo work.
    help="\b\n" + LOGO + "\n" + HELP,
    epilog=f"Default shellcheck command: {' '.join(DEFAULT_COMMAND)!r}",
)
@click.version_option(__version__)
@click.option(
    "-f",
    "--file",
    "files",
    type=GlobFileType("rb"),
    multiple=True,
    help="Specify one or more .gitlab-ci.yml files. Default to .gitlab-ci.yml in the current working directory. Use - for stdin. "
    "Can be specified multiple times and supports resolving (recursive) shell wildcards (via glob.).",
    default=[".gitlab-ci.yml"],
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=click.IntRange(min=0, max=len(VERBOSE_OPTIONS) - 1),
    help="Increase logging verbosity on stderr (use once for INFO, twice for DEBUG).",
)
@click.option(
    "--cmd",
    help="Overwrite the default shellcheck command. "
    "Must be specified as a single command that will be split into arguments via shlex.split. "
    "Take care to set the output format to json1 and take input from stdin.",
)
@click.option(
    "-i",
    "--includes",
    type=click.Choice(IncludeMode, case_sensitive=False),
    help=IncludeMode.__doc__,
    default=IncludeMode.IGNORE_REMOTE,
)
@click.option(
    "--check-args-for-files/--dont-check-args-for-files",
    default=True,
    show_default=True,
    help="Error if args contains any files. This should almost never be disabled.",
)
@click.option(
    "-w",
    "--wrap",
    "--width",
    # If we get an absurdly small value from the autodetect, set to a more sane default rather than clamping to minimum.
    # Unfortunately this leaks a global, but it's the most compact way to still keep the good click type checker behaviour.
    default=_w if (_w := shutil.get_terminal_size(fallback=(DEFAULT_WRAP, 50)).columns) >= MINIMUM_WRAP else DEFAULT_WRAP,
    type=click.IntRange(min=MINIMUM_WRAP),
    show_default=True,
    help="Set wrapping width on script output. Default is to autodetect with a fallback to {DEFAULT_WRAP} in case of absurdly small values.",
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(
    files: Tuple[Tuple[BinaryIO]], verbose: int, cmd: str, includes: IncludeMode, check_args_for_files: bool, wrap: int, args: Tuple[str]
):
    # Logging framework is used for issues & debugging only, and outputs to stderr.
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=VERBOSE_OPTIONS[verbose])
    log = logging.getLogger("glscpc")

    # Multiple -f parameters can return multiple files, but we just want a single iterator, so chain them.
    files = tuple(itertools.chain(*files))

    if ASCII_ONLY:
        click.echo(f"GLSCPC by Qteal - v{__version__} - ASCII only")
    else:
        click.echo(LOGO)

    dbg = (files, verbose, cmd, includes, check_args_for_files, wrap, args)
    log.debug("Arguments: files=%r, verbose=%r cmd=%r includes=%r, check_args_for_files=%r, wrap=%r, args=%r", *dbg)
    del dbg

    if check_args_for_files:
        # A common bug in the invocation of glscpc is to specify the -f once and then use a glob. This puts only the first argument in files
        # option and puts the rest in args. This leads to strange behaviour, if not outright ignored files. To combat this, we check if
        # any argument to be passed to shellcheck is actually a file on disk. This should almost never be a legitimate argument, but in case
        # it should be, there is an option to disable this check. To provide similar functionality without resorting to xargs / find, we
        # resolve globs ourselves. This is a design flaw in the CLI, but I don't want to break backwards compatability.
        for arg in args:
            if os.path.exists(arg):
                click.secho(
                    f"Argument {arg!r} is a file. Arguments are options for shellcheck, use '-f' to change the input file.\n"
                    "Beware wildcards/globs, as they expand to multiple arguments without the required '-f' in between. Quote the "
                    "expression to let glscpc handle it instead of the shell.\n"
                    "If this is a false positive, run with '--dont-check-args-for-files' to disable this check.",
                    fg="bright_red",
                )
                raise Exit(3)

    if cmd is None:
        cmd = DEFAULT_COMMAND
        log.debug("No shellcheck command provided, defaulting to %r", cmd)
    else:
        cmd = shlex.split(cmd)
    cmd.extend(args)
    log.debug("Full command with arguments: %r", cmd)

    # A quick (not entirely bulletproof) sanity check, before we start computing.
    if shutil.which(cmd[0]) is None:
        click.secho(f"Cannot find executable {cmd[0]!r}. Is it installed?", fg="bright_red")
        raise Exit(2)

    exit_code = 0
    codes = set()
    for file in files:
        # Only skip newline if verbosity is 0, that way everything can print on a single line if there is no problems.
        # But if we're verbose, there will be stderr log lines interleaved. Adding a newline makes that easier to read.
        click.secho(f"Processing {click.format_filename(file.name)}... ", fg="yellow", nl=verbose != 0)
        try:
            checker = Checker(cmd, includes, wrap)
            text = "\n".join(transform_return(r) for r in checker.process(file))
            codes.update(x["code"] for x in checker.issues)
        except Exception as e:
            log.debug("Fatal error", exc_info=True)
            text = transform_return(e)
        if text:
            exit_code = 1
            click.secho("FAIL", fg="bright_red")
            click.echo(text)
        else:
            click.secho("OK", fg="bright_green")
    if codes:
        click.echo("Issue help urls:")
        for code in sorted(codes):
            click.echo(transform_return(f"• [SC{code}](https://www.shellcheck.net/wiki/SC{code})"))
    raise Exit(exit_code)


if __name__ == "__main__":
    main()
