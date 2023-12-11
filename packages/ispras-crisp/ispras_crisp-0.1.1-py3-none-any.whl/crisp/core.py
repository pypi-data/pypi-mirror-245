import os
import subprocess
from typing import List

import git
import pycodestyle
from colorama import Fore, Style
from wcmatch.fnmatch import fnmatch
from wcmatch.glob import globmatch

from crisp import CrispError
from crisp.config import CrispConfig, FileSelectionMode, process_config
from crisp.report import CustomPycodestyleReport, print_report

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def run_crisp(action: str, mode: FileSelectionMode, workdir: str = ".") -> None:
    """Запуск Crisp в режиме ``action``.

    :param action: режим (``lint`` для проверки или ``fix`` для исправления файлов)
    :param mode: стратегия выбора файлов
    :param workdir: директория проверяемого Git-репозитория либо одна из ее
        поддиректорий
    :raises CrispError: в случае отсутствия валидных Git-репозитория и конфигурации

    :group: functions
    """
    git_repo = get_git_repo(workdir)

    os.chdir(git_repo.working_tree_dir)  # pyre-ignore
    config = process_config(git_repo.working_tree_dir)  # pyre-ignore

    files = list_files(git_repo, mode, config)
    if not files:
        print(f"{Fore.LIGHTYELLOW_EX}No files to check.")
        return

    if action == "fix":
        fix(files)
        return

    pycodestyle_guide = pycodestyle.StyleGuide(
        max_line_length=config.line_length,
        ignore=config.ignore_errors_pycodestyle,
        reporter=CustomPycodestyleReport,
    )
    pycodestyle_report = pycodestyle_guide.check_files(files)

    ruff_proc = subprocess.run(
        ["ruff", "check", "--output-format", "json", *files],
        capture_output=True,
        text=True,
    )
    black_proc = subprocess.run(
        ["black", "--check", *files], capture_output=True, text=True
    )
    ruff_output = None if ruff_proc.returncode == 0 else ruff_proc.stdout
    black_output = None if black_proc.returncode == 0 else black_proc.stderr

    print_report(config.workdir, pycodestyle_report, ruff_output, black_output)
    check_unable_to_process(ruff_proc.stderr)


def fix(files: List[str]) -> None:
    """Исправить файлы ``files``.

    :param files: список относительных путей к файлам, которые потенциально будут
        исправлены

    :group: functions
    """
    modified_times = {path: os.stat(path).st_mtime for path in files}

    ruff_proc = subprocess.run(
        ["ruff", "check", "--fix-only", *files], capture_output=True, text=True
    )
    _black_proc = subprocess.run(["black", *files], capture_output=True, text=True)

    fixed_files = sorted(
        p for p, t in modified_times.items() if os.stat(p).st_mtime > t
    )
    if not fixed_files:
        print(f"{Fore.LIGHTYELLOW_EX}Nothing to fix.")
    for path in fixed_files:
        print(f"Fixed {Fore.LIGHTBLUE_EX}{path}")

    check_unable_to_process(ruff_proc.stderr)


def check_unable_to_process(ruff_stderr: str) -> None:
    if len(ruff_stderr) > 0:
        print(f"{Fore.RED}Ruff was unable to process some files:")
        for line in ruff_stderr.strip().split("\n"):
            print(f"    {line}")


def get_git_repo(workdir: str) -> git.Repo:
    try:
        repo = git.Repo(workdir, search_parent_directories=True)
    except git.InvalidGitRepositoryError as err:
        raise CrispError(
            f"Could not find a Git repo in "
            f"{Fore.LIGHTYELLOW_EX}{workdir}{Style.RESET_ALL} or its parents.\n"
            f"Crisp only works in Git repos with {Fore.LIGHTYELLOW_EX}pyproject.toml"
            f"{Style.RESET_ALL} file."
        ) from err

    if repo.bare:
        raise CrispError("Bare Git repos are not supported.")

    return repo


def list_files(
    git_repo: git.Repo, mode: FileSelectionMode, config: CrispConfig
) -> List[str]:
    """Получить список *существующих* файлов для обработки.

    Функция должна запускаться только с корневой директорией Git-репозитория в качестве
    текущей рабочей директории ``os.getcwd()``.

    :param git_repo: Git-репозиторий
    :param mode: стратегия выбора файлов
    :param config: конфигурация Crisp
    :raises CrispError: в случае невалидности Git-репозитория (например, отсутствия
        коммитов)

    :group: functions
    """

    def _from_working_tree(include_staged):
        if include_staged:
            against = "HEAD" if git_repo.head.is_valid() else EMPTY_TREE_SHA
            return git_repo.git.diff(against, name_only=True)
        else:
            return git_repo.git.diff(None, name_only=True)

    def _from_commit_diff(branch):
        if not git_repo.head.is_valid():
            raise CrispError(
                "Repo "
                f"{Fore.LIGHTYELLOW_EX}{git_repo.working_tree_dir}{Style.RESET_ALL} "
                "has no commits."
            )
        if not git_repo.head.commit.parents:
            against = EMPTY_TREE_SHA
        elif branch is not None:
            against = branch
        else:
            against = "HEAD~1"

        return git_repo.git.diff(f"{against}..HEAD", name_only=True)

    if mode == FileSelectionMode.default:
        comma_sep = _from_working_tree(include_staged=True)
    elif mode == FileSelectionMode.modified:
        comma_sep = _from_working_tree(include_staged=False)
    elif mode == FileSelectionMode.latest_commit:
        comma_sep = _from_commit_diff(branch=None)
    elif mode == FileSelectionMode.diff_master:
        comma_sep = _from_commit_diff(branch=config.default_branch)
    else:
        comma_sep = git_repo.git.ls_files()

    result = comma_sep.split("\n")
    return exclude_files([f for f in result if os.path.isfile(f)], config.exclude_files)


def exclude_files(files: List[str], patterns: List[str]) -> List[str]:
    result = []

    for path in files:
        if not fnmatch(os.path.basename(path), "*.py"):
            continue

        is_excluded = False
        for pattern in patterns:
            is_dir = pattern.endswith(os.sep)
            pattern = os.path.splitdrive(os.path.normpath(pattern))[1]
            is_relpath = os.path.basename(pattern) != pattern

            if is_relpath:
                if is_dir:
                    pattern = os.path.join(pattern, "**")
                is_excluded = globmatch(path, pattern)
            else:
                parts = path.split(os.sep)
                if is_dir:
                    del parts[-1]
                for part in parts:
                    is_excluded = fnmatch(part, pattern)
                    if is_excluded:
                        break
            if is_excluded:
                break
        if not is_excluded:
            result.append(path)

    return result
