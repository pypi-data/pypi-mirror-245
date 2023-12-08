from typing import Callable, Any


class ArgumentDummy:
    kind: str

    def __init__(self, kind: str):
        if kind is None:
            raise ValueError("ArgumentDummy.__init__: Kind can not be None!")

        self.kind = kind


class FileArgumentDummy(ArgumentDummy):
    _lambda: Callable[..., Any]

    def __init__(self, kind: str):
        self._lambda = lambda input: input
        super().__init__(kind)

    def get_lambda(self) -> Callable[..., Any]:
        return self._lambda
