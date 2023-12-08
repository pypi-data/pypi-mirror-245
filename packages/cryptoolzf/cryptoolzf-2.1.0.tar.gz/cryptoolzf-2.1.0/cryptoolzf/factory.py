# postpone evaluation of annotations
from __future__ import annotations

from typing import Any, Generic, TypeVar, Optional, Callable, Generator, List

from .base import AdHoc

from queue import Queue

FactoryItem = TypeVar("FactoryItem")


class Factory(Queue, Generic[FactoryItem]):
    constructor: Callable[..., FactoryItem]

    _handle_exception: Callable[[Exception], None]

    defaults: Optional[dict[str, Any]] = None

    stored: List[FactoryItem] = []

    def __init__(
        self,
        constructor: Callable[..., FactoryItem],
        exception_handler: Callable[[Exception], None] = None,
        defaults: Optional[dict[str, Any]] = None,
        maxsize=0,
    ):
        super().__init__(maxsize)

        self.constructor = constructor

        self._handle_exception = exception_handler

        if defaults:
            self.defaults = defaults

    def stream(self, some: int = 0) -> Generator[FactoryItem, None, None]:
        qsize: int = self.qsize()
        some = some or qsize
        predicate = min if qsize else max

        for _ in range(predicate(qsize, some)):
            yield self.create()

    def create(self, store: bool = False) -> FactoryItem:
        result = None

        data_dict = self.defaults if self.empty() else self.get()

        args = data_dict.get("args") or []

        data_dict.pop("args", None)

        try:
            result = self.constructor(*args, **data_dict)
        except Exception as e:
            if self._handle_exception:
                self._handle_exception(e)
            else:
                raise e

        if store:
            self.stored.append(result)

        return result

    @AdHoc.ListMorph(0)
    def put(
        self,
        item: Any,
        block: bool = True,
        timeout: Optional[float] = None,
    ):
        super().put(item, block=block, timeout=timeout)
