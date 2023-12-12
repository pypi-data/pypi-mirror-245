import argparse
import sys

from colorama import Fore, Style

from crisp.config import FileSelectionMode
from crisp.core import CrispError, run_crisp


def validate_mode(args: dict) -> FileSelectionMode:
    """Валидация аргументов командной строки, связанных со стратегией выбора файлов.

    Функция проверяет, что указано не более одной стратегии.

    :param args: словарь с аргументами командной строки
    :returns: объект :class:`FileSelectionMode` со стратегией
    :raises CrispError: если указано более одной стратегии

    :group: functions
    """
    already_specified_an_option = False
    mode = FileSelectionMode.default

    for mode_str in ["modified", "latest_commit", "diff_master", "all_files"]:
        if args[mode_str] is True:
            if already_specified_an_option:
                raise CrispError(
                    "Specifying more than one file selection option is not allowed."
                )
            already_specified_an_option = True
            mode = FileSelectionMode[mode_str]

    return mode


def main():
    parser = argparse.ArgumentParser(
        description=f"{Fore.LIGHTYELLOW_EX}Coding Rules at ISP{Style.RESET_ALL}"
    )
    parser.add_argument(
        "action",
        default="lint",
        const="lint",
        nargs="?",
        choices=["lint", "fix"],
        help="action (check or fix the files); default: %(default)s",
    )
    parser.add_argument(
        "--workdir", default=".", help="working directory; default: '%(default)s'"
    )

    group = parser.add_argument_group(
        title="File selection options",
        description="Default behavior (no option specified): check uncommitted files",
    )
    group.add_argument(
        "-m",
        "--modified",
        action="store_true",
        help="check modified files only (those not fully staged)",
    )
    group.add_argument(
        "-1",
        "--latest-commit",
        action="store_true",
        help="check files affected by the latest commit",
    )
    group.add_argument(
        "--diff-master",
        action="store_true",
        help="check files from diff between default branch and the latest commit",
    )
    group.add_argument(
        "-a", "--all-files", action="store_true", help="check all files tracked by Git"
    )

    args = vars(parser.parse_args())

    try:
        mode = validate_mode(args)
        sys.exit(run_crisp(args["action"], mode, args["workdir"]))
    except CrispError as err:
        print(
            f"{Fore.LIGHTRED_EX}[{err.__class__.__name__}]{Style.RESET_ALL}: {err}",
            file=sys.stderr,
        )
        sys.exit(2)
