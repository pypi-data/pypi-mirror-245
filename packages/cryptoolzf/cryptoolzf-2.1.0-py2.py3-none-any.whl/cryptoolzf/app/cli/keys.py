import click

from pathlib import Path

from cryptoolzf.utils import process_pem_file, process_naked_b64

from cryptoolzf.app.run import ArgumentDummy, FileArgumentDummy, ToolRunner

from .cryptoolzf import cryptoolzf, help

_keys_help_text = "This tool creates keypairs in encrypted format \
with different formats to choose from, currently. In future, this tool \
will also allow different algorithms and additional key types. \
\n\n Note that this is an ALPHA version, most errors are not handled, \
meaning that if you did something wrong, then python will weirdly error \
out instead of informing you on what exactly happened. We made sure that \
you can't error on some basic things."


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help=_keys_help_text,
)
@click.pass_context
def keys(ctx):
    pass


_keys_create_help_text = "This command creates a keypair for a chosen network and encrypts the secret \
with a chosen algorithm combination (designated by the keyword shown in options), formats it into a \
chosen format, and also writes (depending on format or choice etc.) it into a file or stdout. \
Note that the options may also be appended at the end, but it is advisable to prepend them before commands.\
\n\n NUMBER_PASSPHRASES is the number of passphrases used for key creation. We demand either 1 passphrase \
for all keys, or multiple passphrases, for the SAME NUMBER_KEYS_CREATED."


@click.command(help=_keys_create_help_text)
@click.argument(
    "number_passphrases",
    type=int,
    required=False,
    default=1,
    nargs=1,
)
@click.argument(
    "number_keys_created",
    nargs=1,
    required=False,
    type=int,
    default=1,
)
@click.option(
    "-n",
    "--network",
    nargs=1,
    required=False,
    type=click.Choice(["ethereum"]),
    default="ethereum",
    help="The network to create keys for.",
)
@click.option(
    "-a",
    "--algorithm",
    nargs=1,
    required=False,
    type=click.Choice(["aesgcm"]),
    default="aesgcm",
    help="The keyword for the set of algorithms which should be used. For example, aesgcm is currently pbdkf2 + aesgcm.",
)
@click.option(
    "-f",
    "--format",
    nargs=1,
    type=click.Choice(["pem", "qr"]),
    required=False,
    default="pem",
    help="The default output format for encrypted data.",
)
@click.option(
    "-o",
    "--outfile",
    nargs=1,
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
    required=False,
    default=None,
    help="The file to print the created data to.",
)
@click.option(
    "--header",
    nargs=1,
    type=str,
    required=False,
    default=None,
    help="The custom header to use for PEM blocks.",
)
@click.option(
    "--digest/--no-digest",
    type=bool,
    required=False,
    default=False,
    help="Before encryption, compute the digest of the private key. Currently only a dummy option. NOTE: Do NOT send this with encrypted text.",
)
def create(
    number_passphrases,
    number_keys_created,
    network,
    algorithm,
    format,
    outfile,
    header,
    digest,
):
    if digest:
        click.echo("keys :: digest is a dummy option, development ongoing!")
        raise click.Abort

    if format == "qr":
        if not outfile:
            click.echo("keys :: QR code requires a filepath!")
            raise click.Abort
        if header:
            click.echo("keys :: QR code does not take a header arg!")
            raise click.Abort

    if number_passphrases != 1:
        if number_passphrases != number_keys_created:
            click.echo(
                "keys :: If more than one passphrase, the number of keys must be equal to the number of passphrases!"
            )
            raise click.Abort

    runner = ToolRunner()

    pass_dummy = ArgumentDummy(f"bpass:utf-8:{number_passphrases}:True:a passphrase")

    runner.run(
        [pass_dummy],
        t="keys",
        mode="create",
        outpath=Path(outfile) if outfile else None,
        algorithm=algorithm,
        network=network,
        digest=digest,
        format=format,
        header=header or "KEYS",
        keynum=number_keys_created,
    )


_keys_reveal_help_text = 'This command is used to decrypt the encrypted format you have received, \
as output of the `create` command into some file or stdout. This format must be pasted into preferably \
ONE file and then given as input to the command, with the right options, according to how you encrypted \
your data.\n\nNOTE that for QR codes, the QR code must be scanned by the user and only the "plaintext" \
cyphertext should be pasted into a file, see the docs for more.\n\nNUMBER_PASSPHRASES is the number of \
passphrases. If this is set to 1, then the passphrase provided will be used on all encrypted files provided. \
Otherwise, the passphrases provided sequentially will also be used in the same sequence to decrypt the data, \
exactly like during encryption.\n\nFILEPATHS are the paths to the files which contain the key data.'


@click.command(help=_keys_reveal_help_text)
@click.argument(
    "number_passphrases",
    nargs=1,
    type=int,
    default=1,
)
@click.argument(
    "filepaths",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
    required=True,
)
@click.option(
    "-n",
    "--network",
    nargs=1,
    type=click.Choice(["ethereum"]),
    required=False,
    default="ethereum",
    help="The network the keys belong to.",
)
@click.option(
    "-a",
    "--algorithm",
    nargs=1,
    type=click.Choice(["aesgcm"]),
    required=False,
    default="aesgcm",
    help="The keyword for the set of algorithms which the data is encrypted with.",
)
@click.option(
    "-f",
    "--format",
    nargs=1,
    type=click.Choice(["pem", "qr"]),
    required=True,
    help="Format of the formatted input cyphertext. In future will be automatic.",
)
@click.option(
    "-o",
    "--outfile",
    nargs=1,
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
    required=False,
    default=None,
    help="The file to print the decrypted data to.",
)
@click.option(
    "--digest/--no-digest",
    type=bool,
    required=False,
    default=False,
    help="Verify private key digest during decryption. Currently a dummy option.",
)
def reveal(number_passphrases, filepaths, network, algorithm, format, outfile, digest):
    if number_passphrases < len(filepaths):
        click.echo(
            "keys :: Can't have more files than passphrases, remove empty files!"
        )
        raise click.Abort

    runner = ToolRunner()

    pass_dummy = ArgumentDummy(
        f"bpass:utf-8:{number_passphrases}:False:the decryption passphrase"
    )
    file_dummy = FileArgumentDummy("file:-1:str:ascii")

    if format == "pem":
        file_dummy._lambda = process_pem_file
    elif format == "qr":
        file_dummy._lambda = process_naked_b64

    runner.run(
        [pass_dummy, file_dummy],
        t="keys",
        mode="reveal",
        f=[Path(p) for p in filepaths],
        outpath=Path(outfile) if outfile else None,
        algorithm=algorithm,
        network=network,
        digest=digest,
        format=format,
    )


keys.add_command(create)
keys.add_command(reveal)
keys.add_command(help)
cryptoolzf.add_command(keys)
