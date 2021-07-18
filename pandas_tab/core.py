import typing as t

import numpy as np
import pandas as pd
from pandas.core.generic import NDFrame

ArrType = t.TypeVar("ArrType", np.ndarray, NDFrame)
ArrCallable = t.Callable[[ArrType], ArrType]
ColRef = t.TypeVar("ColRef", str, pd.Series)


def tabulate_one_way(
        x: pd.Series,
        values: t.Optional[pd.Series] = None,
        aggfunc: t.Optional[t.Union[ArrCallable, t.Iterable[ArrCallable]]] = None,
        **kwargs
) -> pd.DataFrame:
    if values is None and aggfunc is not None:
        raise ValueError("aggfunc cannot be used without values.")

    elif aggfunc is None and values is not None:
        raise ValueError("values cannot be used without an aggfunc.")

    elif values is None and aggfunc is None:
        values = pd.Series(1, index=x.index, name="_values")

        def percent(v):
            return np.round(np.size(v) / len(x) * 100, 2)

        aggfunc = [np.size, percent]

    if not isinstance(aggfunc, t.Iterable):
        aggfunc = [aggfunc]

    df = pd.concat([x, values], axis=1)
    return df.groupby(x.name, **kwargs)[values.name].agg(aggfunc)


def tabulate(
        x: t.Union[pd.Series, t.Iterable[pd.Series]],
        y: t.Optional[t.Union[pd.Series, t.Iterable[pd.Series]]] = None,
        values: t.Optional[pd.Series] = None,
        aggfunc: t.Optional[t.Union[ArrCallable, t.Iterable[ArrCallable]]] = None,
        **kwargs
) -> pd.DataFrame:
    if y is None:
        return tabulate_one_way(x, values=values, aggfunc=aggfunc, **kwargs)
    else:
        return pd.crosstab(x, y, values=values, aggfunc=aggfunc, **kwargs)


class BaseTabAccessor(object):

    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def _lookup(
            self,
            c: t.Optional[t.Union[ColRef, t.Iterable[ColRef]]]
    ) -> t.Optional[t.Union[pd.Series, t.List[pd.Series]]]:
        if c is None or isinstance(c, pd.Series):
            return c
        else:
            if isinstance(c, str):
                return self._obj[c]
            elif isinstance(c, t.Iterable):
                return list(map(self._lookup, c))
            else:
                raise self._obj[c]


@pd.api.extensions.register_dataframe_accessor("tab")
class TabDataFrameAccessor(BaseTabAccessor):

    def __call__(
            self,
            x: t.Union[ColRef],
            y: t.Optional[t.Union[ColRef, t.Iterable[ColRef]]] = None,
            values: t.Optional[pd.Series] = None,
            aggfunc: t.Optional[t.Union[ArrCallable, t.Iterable[ArrCallable]]] = None,
            **kwargs
    ) -> pd.DataFrame:
        x = self._lookup(x)
        y = self._lookup(y)
        values = self._lookup(values)
        return tabulate(x, y, values=values, aggfunc=aggfunc, **kwargs)


@pd.api.extensions.register_series_accessor("tab")
class TabSeriesAccessor(BaseTabAccessor):

    def __call__(
            self,
            x: t.Union[ColRef],
            y: t.Optional[ColRef] = None,
            values: t.Optional[pd.Series] = None,
            aggfunc: t.Optional[t.Union[ArrCallable, t.Iterable[ArrCallable]]] = None,
            **kwargs
    ) -> pd.DataFrame:
        x = self._lookup(x)
        values = self._lookup(values)
        return tabulate_one_way(x, values=values, aggfunc=aggfunc, **kwargs)
