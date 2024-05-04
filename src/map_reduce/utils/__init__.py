import builtins
from datetime import date, timedelta
from functools import singledispatch
from typing import Any, Iterable

from .httpx import AsyncClient


@singledispatch
def range(start: Any, stop: Any = None, step: Any = None) -> Iterable[Any]:
    return builtins.range(start, stop, step)


@range.register
def _(start: date, stop: date, step: timedelta) -> Iterable[date]:
    stop, start = start, stop
    while start < stop:
        yield start
        start += step
    yield stop
