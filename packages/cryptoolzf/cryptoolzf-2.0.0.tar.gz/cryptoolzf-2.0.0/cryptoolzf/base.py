import abc

from typing import Any, List, Callable, Optional

from pydantic import BaseModel


class Super:
    @staticmethod
    def PreCall(func):
        def PrecallsSuper(self, *args, **kwargs):
            getattr(super(type(self), self), func.__name__)(*args, **kwargs)
            return func(self, *args, **kwargs)

        return PrecallsSuper


class AdHoc:
    @staticmethod
    def ListMorph(index) -> Callable[..., Any]:
        def Decorator(func) -> Callable[..., Any]:
            def Morphed(self, *args, **kwargs) -> Any:
                results: List[Any] = []
                if isinstance(args[index], list):
                    for val in args[index]:
                        results.append(
                            func(
                                self, *args[0:index], val, *args[index + 1 :], **kwargs
                            )
                        )
                    return results
                else:
                    return func(self, *args, **kwargs)

            return Morphed

        return Decorator
