import json
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from colorama import Fore, Style
from pycodestyle import StandardReport


@dataclass
class LintError:
    """Датакласс, описывающий ошибку линтинга.

    :group: classes
    """

    line_number: int  #: номер строки, в которой имеется ошибка
    offset: int  #: номер столбца (символа) в этой строке

    error_code: str
    """
    код ошибки; см. списки кодов `Ruff <https://docs.astral.sh/ruff/rules/>`_
    и `pycodestyle <https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes>`_
    """

    message: str  #: текст сообщения об ошибке


class CustomPycodestyleReport(StandardReport):
    """Обертка над отчетом pycodestyle.

    В классе имеется дополнительный атрибут ``lint_errors`` --- словарь, хранящий для
    каждого относительному пути (ключ) к проверяемому файлу список (значение) найденных
    в файле ошибок :class:`.LintError`.

    :group: classes
    """

    def __init__(self, options) -> None:
        super().__init__(options)
        self.lint_errors: Dict[str, List[LintError]] = defaultdict(list)

    def get_file_results(self) -> None:
        """Переопределение метода базового класса ``pycodestyle.StandardReport``.

        Вместо печати всех ошибок для одного файла, как это делается в базовом классе,
        эти ошибки добавляются в общий для всех файлов словарь ``lint_errors``.
        """
        for line_number, offset, error_code, message, _doc in self._deferred_print:
            self.lint_errors[self.filename].append(
                LintError(line_number, offset, error_code, message)
            )


def print_report(
    workdir: str,
    pycodestyle_report: CustomPycodestyleReport,
    ruff_output: Optional[str] = None,
    black_output: Optional[str] = None,
) -> int:
    """Распечатать отчет о проверке файлов на ошибки линтинга.

    :param workdir: путь к директории с проверенным Git-репозиторием
    :param pycodestyle_report: отчет с ошибками линтинга pycodestyle
    :param ruff_output: вывод команды Ruff; его наличие означает наличие ошибок из
        групп, проверяемых Ruff
    :param black_output: вывод команды Black; его наличие означает, что файл требует
        переформатирования
    :returns: 0 при отсутствии ошибок линтинга, 1 иначе

    :group: functions
    """
    lint_errors: Dict[str, Tuple[List[LintError], bool]] = {}

    for path in pycodestyle_report.lint_errors:
        lint_errors[path] = (pycodestyle_report.lint_errors[path], False)

    if ruff_output is not None:
        for ruff_error in json.loads(ruff_output):
            path = os.path.relpath(ruff_error["filename"], workdir)
            lint_error = LintError(
                ruff_error["location"]["row"],
                ruff_error["location"]["column"],
                ruff_error["code"],
                ruff_error["message"],
            )
            if path not in lint_errors:
                lint_errors[path] = ([lint_error], False)
            else:
                lint_errors[path][0].append(lint_error)

    if black_output is not None:
        for line in black_output.split("\n"):
            if line.startswith("would reformat "):
                path = os.path.relpath(line[len("would reformat ") :], workdir)
                if path not in lint_errors:
                    lint_errors[path] = ([], True)
                else:
                    file_lint_errors = lint_errors[path][0]
                    lint_errors[path] = (file_lint_errors, True)

    if not lint_errors:
        print(f"{Fore.LIGHTGREEN_EX}All good!")
        return 0

    for path, (file_lint_errors, needs_black) in sorted(
        lint_errors.items(), key=lambda err: err[0]
    ):
        print(f"{Fore.LIGHTBLUE_EX}{path}")

        for lint_error in sorted(
            file_lint_errors, key=lambda err: (err.line_number, err.offset)
        ):
            print(
                f"    {lint_error.line_number}{Style.DIM}:{lint_error.offset}: "
                f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}{lint_error.error_code} "
                f"{Style.RESET_ALL}{lint_error.message}"
            )
        if needs_black:
            print(f"    {Fore.LIGHTRED_EX}needs Black reformatting")
    return 1
