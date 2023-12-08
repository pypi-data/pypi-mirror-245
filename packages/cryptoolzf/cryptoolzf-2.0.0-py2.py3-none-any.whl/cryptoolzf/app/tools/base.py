from __future__ import annotations

import abc

from typing import List, Dict, Union, Callable, TypeVar, Any


# Our args will be in list format
Args = List[Any]

# Our options (from kwargs) are in a dict
Options = Dict[str, Any]

# TypeVar for generics
SingleType = TypeVar("SingleType")

# Our registry separates based on command name
Registry = Dict[str, SingleType]

# Handlers are functions that handle opt values
OptHandlers = Dict[str, Callable[List[Any], Any]]

# The registry stores for each command opts
OptHandlerRegistry = Registry[OptHandlers]

# Arg handlers are functions that handle args
ArgHandlers = List[Callable[List[Any], Any]]

# Arg handler list registry with int key
ArgHandlerRegistry = Registry[ArgHandlers]

# Builders build any class instances
BuilderDict = Dict[str, Callable[..., Any]]

# Registry for them
BuilderRegistry = Registry[BuilderDict]


class PreDirector:
    # static
    _opt_handlers_registry: OptHandlerRegistry = {}
    _arg_handlers_registry: ArgHandlerRegistry = {}
    _builder_registry: BuilderRegistry[Options] = {}

    # dynamic
    args: Args
    options: Options

    def __init__(self, name: str, args: Args, options: Options):
        self.args = [None] * len(args)

        for key, value in options.items():
            handler = self._opt_handlers_registry.get(name)
            handler = handler and handler.get(key)
            if handler:
                options.update({key: handler(value)})
            else:
                options.update(
                    {key: self._opt_handlers_registry["default"][key](value)}
                )

        self.options = options

        for i in range(len(args)):
            handler = self._arg_handlers_registry.get(name)
            handler = handler and handler.get(i)
            if not handler:
                handler = self._arg_handlers_registry["default"][i]
            if handler:
                self.args[i] = handler(self.options, args)
            else:
                self.args[i] = args[i]
        self.name = name

    def get_instance(self, instance_name: str, *args: Args, **options: Options) -> Any:
        return self._builder_registry[instance_name](*args, **options)

    @classmethod
    def register_builder(cls, key: str, builder: Callable[..., Any]) -> None:
        cls._builder_registry.update({key: builder})

    @classmethod
    def register_opt_handlers(cls, key: str, handlers: OptHandlers) -> None:
        cls._opt_handlers_registry.update({key: handlers})

    @classmethod
    def register_arg_handlers(cls, key: str, handlers: ArgHandlers) -> None:
        cls._arg_handlers_registry.update({key: handlers})
