#!/usr/bin/env python3
"""
A Proxy for TomlGuard,
  which allows you to use the default attribute access
  (data.a.b.c)
  even when there might not be an `a.b.c` path in the data.

  Thus:
  data.on_fail(default_value).a.b.c()

  Note: To distinguish between not giving a default value,
  and giving a default value of `None`,
  wrap the default value in a tuple: (None,)
"""

##-- builtin imports
from __future__ import annotations

# import abc
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import weakref
# from copy import deepcopy
# from dataclasses import InitVar, dataclass, field
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generic,
                    Iterable, Iterator, Mapping, Match, MutableMapping,
                    Protocol, Sequence, Tuple, TypeVar,
                    cast, final, overload, runtime_checkable)
from uuid import UUID, uuid1

##-- end builtin imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

from types import UnionType
from tomlguard.utils.trace_helper import TraceHelper
from tomlguard.base import GuardBase
from tomlguard.error import TomlAccessError
from tomlguard.base import TomlTypes

class TomlGuardProxy:
    """
    A Wrapper for guarded access to toml values.
    you get the value by calling it.
    Until then, it tracks attribute access,
    and reports that to GuardBase when called.
    It also can type check its value and the value retrieved from the toml data
    """

    def __init__(self, data:GuardBase, types:Any=None, index:list[str]|None=None, fallback:TomlTypes|None=None):
        self._types                       = types or Any
        self._data                        = data
        self.__index : list[str]            = index or ["<root>"]
        self._fallback                    = fallback
        if fallback:
            self._match_type(fallback)

    def __repr__(self) -> str:
        type_str = self._types_str()
        index_str = ".".join(self._index())
        return f"<TomlGuardProxy: {index_str}:{type_str}>"

    def __call__(self, wrapper:callable[[TomlTypes], Any]|None=None) -> Any:
        self._notify()
        wrapper : callable[[TomlTypes], TomlTypes] = wrapper or (lambda x: x)
        match self._data, self._fallback:
            case GuardBase(), _:
                val = self._data
            case (None,), None:
                raise ValueError("No Value, and no fallback")
            case (None,), (None,):
                val = None
            case (None,), data:
                val = data
            case None, _:
                val = None
            case GuardBase() as data, _:
                val = dict(data)
            case _ as data, _:
                val = data

        wrapped = wrapper(val)
        return self._match_type(wrapped)

    def __getattr__(self, attr:str) -> TomlGuardProxy:
        try:
            match self._data:
                case GuardBase():
                    return self._inject(self._data[attr], attr=attr)
                case None:
                    raise TomlAccessError()
                case _:
                    return self._inject(attr=attr)
        except TomlAccessError:
            return self._inject(clear=True, attr=attr)

    def __getitem__(self, keys:str|tuple[str]) -> TomlGuardProxy:
        curr = self
        match keys:
            case tuple():
                for key in keys:
                    curr = curr.__getattr__(key)
            case str():
                curr = self.__getattr__(keys)

        return curr

    def __len__(self) -> int:
        if hasattr(self._data, "__len__"):
            return len(self._data)

        return 0

    def __bool__(self) -> bool:
        return self._data is not None

    def _notify(self) -> None:
        types_str = self._types_str()
        match self._data, self._fallback, self._index():
            case GuardBase(), _, _:
                pass
            case _, _, []:
                pass
            case (None,), val, [*index]:
                GuardBase.add_defaulted(".".join(index), val, types_str)
            case val, _, [*index]:
                GuardBase.add_defaulted(".".join(index), val, types_str)
            case val, flbck, index,:
                raise TypeError("Unexpected Values found: ", val, index, flbck)

    def _types_str(self) -> str:
        match self._types:
            case UnionType() as targ:
                types_str = repr(targ)
            case type(__name__=targ):
                types_str = targ
            case _ as targ:
                types_str = str(targ)

        return types_str

    def _inject(self, val:tuple[Any]=(None,), attr:str|None=None, clear:bool=False) -> TomlGuardProxy:
        new_index = self._index()
        if attr:
            new_index.append(attr)

        match val:
            case (None,):
                val = self._data
            case _:
                pass

        if clear:
            val = (None,)
        return TomlGuardProxy(val, types=self._types, index=new_index, fallback=self._fallback)

    def _match_type(self, val:TomlTypes) -> TomlTypes:
        if val == (None,):
            val = None

        if self._types != Any and not isinstance(val, self._types):
            types_str = self._types_str()
            index_str  = ".".join(self.__index + ['(' + types_str + ')'])
            err = TypeError("TomlProxy Value doesn't match declared Type: ", index_str, val, self._types)
            raise err.with_traceback(TraceHelper()[5:10])

        return val

    def _index(self) -> list[str]:
        return self.__index[:]

    def _update_index(self, attr:str) -> None:
        self.__index.append(attr)
