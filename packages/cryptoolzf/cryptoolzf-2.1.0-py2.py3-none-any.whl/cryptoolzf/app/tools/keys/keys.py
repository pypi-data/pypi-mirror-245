from typing import Any
from ..base import Args, Options
from .base import PreDirector
from .dropins import *


class Keys:
    @staticmethod
    def run(*args: Args, **options: Options) -> Any:
        director = PreDirector(options.get("network"), args, options)
        runner = director.get_instance(options.get("network"), director)
        return runner.run()
