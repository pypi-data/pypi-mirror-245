from functools import reduce

import pandas as pd

from .constants import PREFIX_SEP
from .meta_base import ColMeta
from .util import camel_to_snake


class ColAccessor(metaclass=ColMeta):
    """describe and access raw columns

    useful for
    - getting column names from static analysis
    - documenting types
    - dry describing nested structures

    e. g.

    >>> class LocationCols(ColAccessor):
    ...     lon = float
    ...     lat = float

    >>> class TableCols(ColAccessor):
    ...     col1 = int
    ...     col2 = str
    ...     foreign_key1 = "name_of_key"
    ...
    ...     class NestedCols(ColAccessor):
    ...         s = str
    ...         x = float
    ...
    ...     start_loc = LocationCols
    ...     end_loc = LocationCols

    >>> TableCols.start_loc.lat
    'start_loc__lat'

    """


class ColAssigner(ColAccessor):
    """define functions that create columns in a dataframe

    later the class attributes can be used to access the column
    can be used to created nested structures of columns

    either by assigning or inheriting within:

    class MyStaticChildAssigner(ColAssigner):

        pass

    class MyAssigner(ColAssigner):

        class MySubAssigner(ColAssigner):
            pass

        chass1 = MyStaticChildAssigner
    """

    def __call__(self, df: pd.DataFrame, carried_prefixes=()) -> pd.DataFrame:
        # dir() is alphabetised object.__dir__ is not
        # important here if assigned cols rely on each other
        return self._assign_cols(self.__dir__(), df, carried_prefixes)

    @staticmethod
    def _call_att(att, df):
        return att(df)

    def _assign_cols(self, cols, df, carried_prefixes):
        return reduce(self._reducer, cols, (df, carried_prefixes))[0]

    def _reducer(self, red_out: tuple[pd.DataFrame, tuple], attid: str):
        if attid.startswith("_"):
            return red_out
        df, prefixes = red_out
        att = getattr(self, attid)
        if isinstance(att, ColMeta):
            inst = att(df, self) if ChildColAssigner in att.mro() else att()
            odf = inst(df, carried_prefixes=(*prefixes, camel_to_snake(attid)))
        elif callable(att):
            col_name = PREFIX_SEP.join((*prefixes, getattr(type(self), attid)))
            odf = df.assign(**{col_name: self._call_att(att, df)})
        else:
            odf = df
        return (odf, prefixes)


class ChildColAssigner(ColAssigner):
    """assigner specifically for nested structures

    methods of these are not called with parameters

    the dataframe and the parent assigner are passed
    to the __init__ method as parameters
    """

    def __init__(self, df: pd.DataFrame, parent_assigner: ColAssigner) -> None:
        pass

    @staticmethod
    def _call_att(att, _):
        return att()
