import abc

# Some types we need for type hints
from typing import List, Optional, Any

from secrets import token_hex

# We use this to manage complexity at least to a certain level
from cryptoolzf.app.tools.base import PreDirector

# For the base Keypair
from pydantic import SecretBytes, BaseModel

# Object which formats and sends output to either file or stdout
from cryptoolzf.printer import Printer, PlainWriter, HexWriter, PEMWriter, QRCodeWriter


def handle_mode_opt(mode: str):
    if not mode:
        raise ValueError("keys.run: No command to run picked!")
    return mode


PreDirector.register_opt_handlers(
    "default",
    {
        "_get": lambda get: get or False,
        "mode": handle_mode_opt,
        "outpath": lambda outpath: outpath,
        "algorithm": lambda algorithm: algorithm,
        "network": lambda network: network,
        "digest": lambda digest: digest,
        "format": lambda format: format,
        "header": lambda header: header and header.upper(),
        "keynum": lambda keynum: keynum,
    },
)


def handle_passphrases_arg(options, args):
    passphrases = args[0]

    n_passphrases = len(passphrases)

    single_passphrase = n_passphrases == 1

    if len(args) == 2:
        options["keynum"] = len(args[1])

    if options.get("keynum"):
        if not single_passphrase and options["keynum"] != n_passphrases:
            print(
                "keys :: There must be either one passphrase for each encrypted key or the number of passphrases must equal the number of keys!"
            )
            exit(1)
    else:
        options["keynum"] = n_passphrases

    if single_passphrase:
        single_pass_value = passphrases[0]

        for _ in range(1, options["keynum"]):
            passphrases.append(single_pass_value)
    return passphrases


PreDirector.register_arg_handlers("default", [handle_passphrases_arg, None])


def build_plain_printer():
    return Printer[PlainWriter]()


def build_hex_printer():
    return Printer[HexWriter]()


def build_pem_printer(*args):
    printer = Printer[PEMWriter]()
    if 0 < len(args):
        printer.writer.set_format([args[0]] * 2)
    else:
        printer.writer.set_format([""] * 2)
    return printer


def build_qr_printer():
    return Printer[QRCodeWriter]()


PreDirector.register_builder("plain_printer", build_plain_printer)
PreDirector.register_builder("hex_printer", build_hex_printer)
PreDirector.register_builder("pem_printer", build_pem_printer)
PreDirector.register_builder("qr_printer", build_qr_printer)


class Keypair(BaseModel, abc.ABC):
    private_key: SecretBytes
    private_key_digest: Optional[bytes] = None
    public_key: str

    def __init__(self, hash_fn: Any = None, **kwargs):
        private_key = self.gen_private_key()

        private_key_digest = None

        if hash_fn:
            private_key_digest = self.calc_private_key_digest(private_key, hash_fn)

        public_key = self.calc_public_key(private_key)

        super().__init__(
            private_key=private_key,
            private_key_digest=private_key_digest,
            public_key=public_key,
        )

    @abc.abstractmethod
    def calc_public_key(self, private_key: SecretBytes) -> None:
        pass

    @abc.abstractmethod
    def gen_private_key(self) -> SecretBytes:
        pass

    def calc_private_key_digest(
        self, private_key: SecretBytes, hash_fn: Any
    ) -> Optional[bytes]:
        return None
