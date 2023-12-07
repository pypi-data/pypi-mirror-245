from abc import ABCMeta
from functools import partial
from itertools import chain
from typing import TypeVar

from .constants import DEFAULT_PP, FORBIDDEN_NAMES, PREFIX_SEP
from .type_hinting import get_return_hint
from .util import camel_to_snake

T = TypeVar("T")


class ColMeta(ABCMeta):
    def __new__(cls, name, bases, local):
        for attr in local:
            if (attr in FORBIDDEN_NAMES) or (
                PREFIX_SEP in attr and not attr.startswith("_")
            ):
                raise ValueError(
                    f"Column name can't be either {FORBIDDEN_NAMES}. "
                    f"And can't contain the string {PREFIX_SEP}. "
                    f"{attr} is given"
                )
        return super().__new__(cls, name, bases, local)

    def __init__(self, name: str, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        self._parent_prefixes = namespace.get("_parent_prefixes", DEFAULT_PP)

    def __getattribute__(cls, attid):
        "so that Cls.xy returns a string for column access"

        att_value = super().__getattribute__(attid)
        if attid.startswith("_") or (attid in FORBIDDEN_NAMES):
            return att_value

        new_pref_arr = (*cls._parent_prefixes, camel_to_snake(attid))

        if isinstance(att_value, ColMeta):

            class _C(att_value):
                _parent_prefixes = new_pref_arr

            return _C

        return_hint_str = get_hint_str(att_value)

        return PREFIX_SEP.join(filter(None, (*new_pref_arr, return_hint_str)))

    def __repr__(cls) -> str:
        base = super().__repr__()
        return base + f" ({', '.join(cls.__col_dir__())})"

    def __getitem__(cls: T, k) -> T:
        class _C(cls):
            _parent_prefixes = (
                *cls._parent_prefixes,
                camel_to_snake(cls.__name__),
                str(k),
            )

        return _C

    def __getcoltype__(cls, attid):
        colval = super().__getattribute__(attid.split(PREFIX_SEP)[-1])
        return colval

    def __col_dir__(cls):
        return [k for k in dir(cls) if not k.startswith("_")]

    def __col_dir_sub__(cls):
        return [k for k in cls.__dict__.keys() if not k.startswith("_")]


def get_all_cols(cls: ColMeta):
    """returns a list of strings of all columns given by the type

    can also be used for nested structues of columns
    """
    return _expand_attid(cls, cls.__col_dir__())


def get_new_cols(cls: ColMeta):
    return _expand_attid(cls, cls.__col_dir_sub__())


def _expand_attid(cls: ColMeta, attlist: list):
    return list(chain(*map(partial(_iter_att_id, cls), attlist)))


def _iter_att_id(cls, attid):
    attval = getattr(cls, attid)
    if isinstance(attval, ColMeta):
        return get_all_cols(attval)
    return [attval]


def get_att_value(accessor: ColMeta, attname: str):
    """get the true assigned value for the class attribute"""
    return accessor.__getcoltype__(attname)


def get_hint_str(val):
    return_hint = get_return_hint(val)
    if isinstance(return_hint, ColMeta):
        cols = get_all_cols(return_hint)
        if len(cols) != 1:
            raise ValueError(f"cols in {return_hint} is not 1 : {cols}")
        return cols[0]
    if isinstance(return_hint, str):
        return return_hint
