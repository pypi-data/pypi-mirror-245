from typing import Optional

from .. import ser
from ..sess import eval_lua_method_factory


method = eval_lua_method_factory('multishell.')


__all__ = (
    'getCurrent',
    'getCount',
    'launch',
    'setTitle',
    'getTitle',
    'setFocus',
    'getFocus',
)


def getCurrent() -> int:
    return method('getCurrent').take_int()


def getCount() -> int:
    return method('getCount').take_int()


def launch(environment: dict, programPath: str, *args: str) -> int:
    args = tuple(ser.encode(a) for a in args)
    return method('launch', environment, ser.encode(programPath), *args).take_int()


def setTitle(tabID: int, title: str):
    return method('setTitle', tabID, ser.encode(title)).take_none()


def getTitle(tabID: int) -> Optional[str]:
    return method('getTitle', tabID).take_option_string()


def setFocus(tabID: int) -> bool:
    return method('setFocus', tabID).take_bool()


def getFocus() -> int:
    return method('getFocus').take_int()
