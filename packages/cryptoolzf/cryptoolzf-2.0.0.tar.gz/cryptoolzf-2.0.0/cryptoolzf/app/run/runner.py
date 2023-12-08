from typing import Any, Optional, Union, List, Callable

# For processing filepaths
from pathlib import Path

# Function to get user input from console
from getpass import getpass

# Using secret values for input as much as possible
from pydantic import SecretBytes, SecretStr

# These dummies represent arguments which should be
# received from the user or files dinamically
from .dummies import ArgumentDummy, FileArgumentDummy

# Import all tool modules
from cryptoolzf.app.tools import Tools


class ToolRunner:
    """
    This class is an opt handler and tool executor, so a bridge between the cli
    and the tools.

    :param get_lambdas: holds lambdas which are used for processing files
        or getting user input, this is such that one may modify them on the go.
    """

    get_lambdas: dict[str, Callable[..., Any]]

    def __init__(self) -> None:
        # Default lambdas
        self.get_lambdas = {
            "int": lambda format, encoding: input(format),
            "str": lambda format, encoding: input(format),
            "pass": lambda format, encoding: SecretStr(getpass(format)),
            "bytes": lambda format, encoding: input(format).encode(encoding),
            "bpass": lambda format, encoding: SecretBytes(
                getpass(format).encode(encoding)
            ),
        }

    def run(self, run_args: List[Any], **run_options) -> Any:
        """This prepares data for and runs a tool module by passing all
        the arguments and options it requires into it's constructor (run_options)
        and run function (run_args).

        :param run_args: The arguments for running the tool wanted by the `t` run
            option. `run_args` can also contain argument dummies, which it recognizes
            and consumes, replacing them with the actual arguments wanted. This is
            the way we prompt for stuff like passwords, because we prefer exerting
            control over such behaviour instead of letting click handle it.
        :param run_options: kwargs-like run options which are passed into the
            tool's constructor, there are two important ones:
            t - This is the tool being called.
            f - These are filepaths which complement the file argument dummy.
            We pass them in as such because of convenience, might move
            this into FileDummy later on.
        """
        # Gets
        tool: Optional[str] = run_options.get("t")
        filepaths: Optional[List[Path]] = run_options.get("f") or None

        # Checks
        if not tool:
            raise ValueError(
                f"{tool} :: ToolRunner.run: A tool to execute must be specified!"
            )

        # Pop ToolRunner options
        run_options.pop("t", None)
        run_options.pop("f", None)

        # Replaces Dummies with user inputted data
        for i in range(len(run_args)):
            argument = run_args[i]

            if isinstance(argument, ArgumentDummy):
                kind_chunks = argument.kind.split(":")

                if kind_chunks[0] == "file":
                    run_args[i] = argument._lambda(
                        self.get_file_data(kind_chunks, [tool, filepaths]),
                        [tool, filepaths],
                    )
                elif kind_chunks[0] in self.get_lambdas:
                    run_args[i] = self.get_user_supplied(kind_chunks, [tool])
                else:
                    raise ValueError(
                        f"{tool} :: ToolRunner.run: There is no lambda for this kind!"
                    )

        # run tool
        return Tools[tool].run(*run_args, **run_options)

    def get_user_supplied(
        self, kind_chunks: List[str], context_chunks: List[str]
    ) -> Any:
        """
        A function which returns user inputs based on a kind and context format.
        The format for user inputted is as follows:
            kind_chunks:
                kind:encoding:size:confirm:printed
            context_chunks:
                tool
        """
        result: Any = []

        _lambda = self.get_lambdas[kind_chunks[0]]

        size = int(kind_chunks[2])

        print_suffix = lambda index: f" at index [{i}]: " if size != 1 else ": "

        for i in range(0, size):
            result.append(
                _lambda(
                    f"{context_chunks[0]} :: please enter {kind_chunks[4]}{print_suffix(i)}",
                    kind_chunks[1],
                )
            )

            if kind_chunks[3] == "True":
                if result[-1] != _lambda(
                    f"{context_chunks[0]} :: please repeat to confirm: ",
                    kind_chunks[1],
                ):
                    print(f"{context_chunks[0]} :: The inputs must equal, exiting!")
                    exit(1)

        return result

    def get_file_data(
        self, kind_chunks: List[str], context_chunks: List[Union[str, List[Path]]]
    ) -> List[Union[str, bytes]]:
        """
        A function which returns file data based on a kind, lambda and context format.
        The format for processing files is as follows:
            kind_chunks:
                kind:maxread:type:encoding
            context_chunks:
                tool:filepaths

        Argument dummies have to implement a file handling lambda if kind is file.
        """
        results = []

        for po in context_chunks[1]:
            po = po if str(po)[0] == "/" else po.absolute()

            if po.exists():
                with open(str(po), mode="r") as fo:
                    results.append(fo.read(int(kind_chunks[1])))
            else:
                print(
                    f"{context_chunks[0]} :: ToolRunner.get_file_data: Couldn't find {str(po)}! Exiting!"
                )
                exit(1)

        for i in range(0, len(results)):
            if kind_chunks[2] == "bytes":
                results[i] = results[i].encode(kind_chunks[3])

        return results

    def add_lambda(self, key: str, lambda_to_add: Callable[..., Any]):
        self.get_lambdas.update({key: lambda_to_add})

    def remove_lambda(self, key: str):
        self.get_lambdas.pop(key, None)
