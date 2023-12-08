from typing import Callable, Iterable, Optional, TypeVar, Union, overload

T = TypeVar("T")
D = TypeVar("D")


@overload
def first(it: Iterable[T], pred: Optional[Callable[[T], Union[object, None]]] = None) -> T:
    ...


@overload
def first(
    it: Iterable[T], pred: Optional[Callable[[T], Union[object, None]]] = None, *, default: D
) -> Union[T, D]:
    ...


def first(
    it: Iterable[T], pred: Optional[Callable[[T], Union[object, None]]] = None, *, default: D = ...
) -> Union[T, D]:
    f = filter(pred, it)
    if default is ...:
        return next(f)
    return next(f, default)


def firstn(it: Iterable[T], pred: Optional[Callable[[T], Union[object, None]]] = None):
    return first(it, pred, default=None)
