"""Console script for cryptoolzf."""
from typing import List, Tuple, Any

import sys
import click

from pydantic import SecretBytes, SecretStr


def handle_click_opts(
    *arguments: Tuple[Any], **opts_dict: dict[str, List[Any]]
) -> dict[str, Any]:
    for key, val in opts_dict.items():
        for nested in val:
            if nested in arguments:
                opts_dict[key] = arguments[arguments.index(nested) + 1]

    return opts_dict


class SecretStrClickParamType(click.ParamType):
    name = "secret string"

    def convert(self, value, param, ctx):
        try:
            return SecretStr(str(value))
        except:
            self.fail(
                f"cryptoolzf :: click: {value} cannot be converted to a string!",
                param,
                ctx,
            )


class SecretBytesClickParamType(click.ParamType):
    name = "secret string"
    encoding: str

    def __init__(self, encoding: str | None):
        if encoding is None:
            raise ValueError(
                "cryptoolzf :: SecretBytesClickParamType.__init__: encoding can't be none!"
            )
        self.encoding = encoding

    def convert(self, value, param, ctx):
        try:
            return SecretBytes(str(value).encode(self.encoding))
        except:
            self.fail(
                f"cryptoolzf :: click: {value} cannot be converted to a string!",
                param,
                ctx,
            )


ClickSecretStr = SecretStrClickParamType()
ClickSecretBytesASCII = SecretBytesClickParamType("ascii")
ClickSecretBytesUTF8 = SecretBytesClickParamType("utf-8")


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-m", "--module", type=str, nargs=1, required=False)
@click.pass_context
def cryptoolzf(ctx, module):
    pass


@click.command(help="Show this message and exit.")
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


cryptoolzf.add_command(help)
