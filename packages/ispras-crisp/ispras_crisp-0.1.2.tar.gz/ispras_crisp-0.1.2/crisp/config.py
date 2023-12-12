import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, List

import tomlkit
from colorama import Fore, Style
from deepmerge import Merger
from tomlkit.exceptions import TOMLKitError

from crisp import CrispError

DEFAULT_LINE_LENGTH = 88
DEFAULT_MASTER_BRANCH = "master"
DEFAULT_SELECT_RUFF = [
    "A",
    "ARG",
    "B",
    "C4",
    "COM",
    "D",
    "F",
    "I",
    "INP",
    "ISC",
    "N",
    "NPY",
    "Q",
    "RUF013",
    "UP",
]
DEFAULT_IGNORE_RUFF = [
    "B028",
    "B905",
    "COM812",
    "D10",
    "D203",
    "D212",
    "D213",
    "D214",
    "D215",
    "D401",
    "D404",
    "D405",
    "D406",
    "D407",
    "D408",
    "D409",
    "D410",
    "D411",
    "D412",
    "D413",
    "D414",
    "D415",
    "D416",
    "D417",
    "N803",
    "N806",
    "UP030",
    "UP032",
]
DEFAULT_IGNORE_PYCODESTYLE = ["E133", "E203", "E241", "E74", "W503", "W505"]


class FileSelectionMode(Enum):
    """Стратегия выбора файлов с исходным кодом на Python для проверки.

    :group: classes
    """

    default = 1  #: выбор файлов, отличающихся между рабочей директорией и репозиторием
    modified = 2  #: выбор файлов, отличающихся между рабочей директорией и индексом
    latest_commit = 3  #: выбор файлов, затронутых последний коммитом (``HEAD``)
    diff_master = 4  #: выбор файлов из разницы между ``master`` и ``HEAD``
    all_files = 5  #: выбор всех файлов, отслеживаемых Git


@dataclass
class CrispConfig:
    """Датакласс с конфигурацией Crisp.

    :group: classes
    """

    workdir: str  #: корневая директория Git-репозитория
    exclude_files: List[str]  #: список шаблонов путей для исключения из обработки
    line_length: int  #: максимальная допустимая длина строк в файлах
    default_branch: str  #: название главной Git-ветки
    select_errors: List[str]  #: список включаемых кодов ошибок и их префиксов в Ruff
    ignore_errors_ruff: List[str]  #: список игнорируемых кодов и префиксов в Ruff
    ignore_errors_pycodestyle: List[str]  #: список игнорируемых ошибок pycodestyle


class SafeDict:
    """Обертка над словарем с валидацией получаемых по ключу значений.

    :group: classes
    """

    def __init__(self, dict_: dict, prefix: str = "") -> None:
        self.dict = dict_
        self.prefix = prefix

    def get(self, key: str, type_: type = dict) -> Any:
        new_prefix = key if self.prefix == "" else f"{self.prefix}.{key}"

        value = self.dict.get(key)
        if value is None:
            return SafeDict({}, new_prefix) if type_ is dict else None

        if type_ is int:
            try:
                value = int(value)
            except (TypeError, ValueError) as err:
                msg = (
                    f"{Fore.LIGHTYELLOW_EX}{new_prefix}{Style.RESET_ALL} field has "
                    f"invalid type '{value.__class__.__name__}' (expected 'int')."
                )
                raise CrispError(msg) from err
        elif not isinstance(value, type_):
            msg = (
                f"{Fore.LIGHTYELLOW_EX}{new_prefix}{Style.RESET_ALL} field has invalid "
                f"type '{value.__class__.__name__}' (expected '{type_.__name__}')."
            )
            raise CrispError(msg)

        return SafeDict(value, new_prefix) if type_ is dict else value


def process_config(workdir: str) -> CrispConfig:
    """Загрузить и обновить файл ``pyproject.toml`` с конфигурацией Crisp.

    Функция при помощи библиотеки ``tomlkit`` преобразует файл в словарь и считывает
    настройки по ключу ``tool.crisp``. В случае отсутствия той или иной настройке ей
    присваивается значение по умолчанию. Также по настройкам Crisp выводятся
    необходимые настройки Ruff и Black, которые записываются в ``pyproject.toml``

    :param workdir: корневая директория Git-репозитория с ``pyproject.toml``
    :returns: объект-конфигурация Crisp
    :raises CrispError: в случае отсутствия ``pyproject.toml`` или наличия в нем ошибок

    :group: functions
    """
    pyproject_path = os.path.join(workdir, "pyproject.toml")
    if not os.path.isfile(pyproject_path):
        raise CrispError(
            f"Could not find {Fore.LIGHTYELLOW_EX}pyproject.toml{Style.RESET_ALL} "
            "in the present Git repo."
        )
    with open(pyproject_path) as f:
        try:
            pyproject = tomlkit.load(f)
        except TOMLKitError as err:
            raise CrispError(
                f"{Fore.LIGHTYELLOW_EX}{pyproject_path}{Style.RESET_ALL} is not a "
                "valid TOML."
            ) from err

    crisp_toml = SafeDict(pyproject).get("tool").get("crisp")
    exclude = crisp_toml.get("exclude", list) or []
    line_length = crisp_toml.get("line-length", int) or DEFAULT_LINE_LENGTH
    default_branch = crisp_toml.get("default-branch", str) or DEFAULT_MASTER_BRANCH

    exclude_escaped = [re.escape(item).replace("/", "\\/") for item in exclude]
    black_regex = f"/({'|'.join(exclude_escaped)})/"
    pyproject_overwrite = {
        "tool": {
            "crisp": {
                "exclude": exclude,
                "line-length": line_length,
                "default-branch": default_branch,
            },
            "black": {"extend-exclude": black_regex, "line-length": line_length},
            "ruff": {
                "extend-exclude": exclude,
                "line-length": line_length,
                "select": DEFAULT_SELECT_RUFF,
                "ignore": DEFAULT_IGNORE_RUFF,
            },
        }
    }
    Merger([(dict, ["merge"])], ["override"], ["override"]).merge(
        pyproject, pyproject_overwrite
    )
    with open(pyproject_path, "w") as f:
        tomlkit.dump(pyproject, f)

    return CrispConfig(
        workdir,
        exclude,
        line_length,
        default_branch,
        DEFAULT_SELECT_RUFF,
        DEFAULT_IGNORE_RUFF,
        DEFAULT_IGNORE_PYCODESTYLE,
    )
