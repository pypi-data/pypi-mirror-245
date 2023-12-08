from typing import List, Any

from cryptoolzf.app.tools.base import Args, Options, PreDirector

from cryptoolzf.crypto import SecretBytes

from secrets import token_hex

# Cryptograhic circuits and data models which hold our input and output data which are transformed later on
from cryptoolzf.crypto.circuits import (
    EncryptPBDKF2_AESGCM,
    DecryptPBDKF2_AESGCM,
    OutsEncryptAESGCM,
    OutsDecryptAESGCM,
)

# For private to public key calc (gives same results as piper's eth_account.Account.from_key)
from eth_hash.auto import keccak
from coincurve import PublicKey
from eth_utils.address import to_checksum_address as checksum

# An instance factory
from cryptoolzf.factory import Factory

# Printer class
from cryptoolzf.printer import Printer

# The base keypair
from ..base import Keypair

# For picking values out from below
from cryptoolzf.utils import match_value, match_values, get_next_free_po

from cryptoolzf.crypto.exceptions import WrongDecryptionInputs


FORMATS = {
    "CREATE": {
        "PEM": [
            [
                "\nYour {} Public Key:\n\n{}",
                "",
            ],
            [
                "\nYour {} Public Key:\n\n{}\n",
                "Private key digest:\n\n{}\n",
            ],
        ],
        "QR": [
            "\nYour {} Public Key:\n\n{}\n",
        ],
    },
    "REVEAL": "\nThe decrypted private key (note it down!):\n\n{}\n",
}


def create_exception_handler(e: Exception) -> None:
    raise e


def reveal_exception_handler(e: Exception) -> None:
    if isinstance(e, WrongDecryptionInputs):
        print("Decryption unsuccessful! Either the passphrase or settings are wrong!")
        exit(1)
    else:
        raise e


def get_eth_encryptor_aesgcm():
    return Factory[OutsEncryptAESGCM](EncryptPBDKF2_AESGCM(), create_exception_handler)


def get_eth_decryptor_aesgcm():
    return Factory[OutsDecryptAESGCM](DecryptPBDKF2_AESGCM(), reveal_exception_handler)


class EthKeypair(Keypair):  # TODO: pk digest, trash eth_hash
    def calc_public_key(self, private_key: SecretBytes) -> str:
        if private_key is None:
            return None

        hex_addr = PublicKey.from_valid_secret(private_key.get_secret_value()).format(
            compressed=False
        )[1:]

        return str(checksum(keccak(hex_addr)[-20:].hex()))

    def gen_private_key(self) -> SecretBytes:
        return SecretBytes(bytes.fromhex(token_hex(32)))


class EthKeys:
    director: PreDirector

    def __init__(self, director: PreDirector):
        self.director = director

    def run(self) -> Any:
        command = self.director.options["mode"]
        if command == "create":
            return self.create()
        elif command == "reveal":
            return self.reveal()

    def create(self) -> Any:
        encrypt_outs = []
        options = self.director.options
        results = None

        # Encrypt
        if options["algorithm"] == "aesgcm":
            encrypt_outs = self._encrypt_aesgcm(options)

        # Print
        if options["format"] == "pem":
            results = self._print_create_pem(options, encrypt_outs)
        elif options["format"] == "qr":
            results = self._print_create_qr(options, encrypt_outs)
        return results

    def reveal(self) -> Any:
        results = None
        decrypt_outs = []
        options = self.director.options
        printer = self.director.get_instance(f"{options['format']}_printer")

        # Decode
        decoder = printer.writer
        self.director.args[1] = [
            decoder.decode(cyphertext) for cyphertext in self.director.args[1]
        ]

        # Decrypt
        if options["algorithm"] == "aesgcm":
            decrypt_outs = self._decrypt_aesgcm(options)

        # Print
        return self._print_reveal_plain(options, decrypt_outs)

    def _encrypt_aesgcm(self, options: Options) -> Any:
        keypairs = [EthKeypair() for _ in range(options["keynum"])]
        encryptor = get_eth_encryptor_aesgcm()
        passphrases = self.director.args[0]
        outputs = []

        for i in range(options["keynum"]):
            encryptor.put(
                {
                    "pbdkf2_passphrase": passphrases[i],
                    "aesgcm_plaintext": keypairs[i].private_key,
                }
            )

            outputs.append(
                [
                    keypairs[i].public_key,
                    keypairs[i].private_key_digest,
                    encryptor.create().aesgcm_cyphertext,
                ]
            )
        return outputs

    def _decrypt_aesgcm(self, options: Options) -> Any:
        passphrases = self.director.args[0]
        cyphertexts = self.director.args[1]
        decryptor = get_eth_decryptor_aesgcm()
        outputs = []

        for i in range(options["keynum"]):
            decryptor.put(
                {
                    "pbdkf2_passphrase": passphrases[i],
                    "aesgcm_cyphertext": cyphertexts[i],
                }
            )

            outputs.append(decryptor.create().aesgcm_plaintext)
        return outputs

    def _print_create_pem(self, options: Options, encrypt_outs: List[Any]) -> Any:
        formats = FORMATS["CREATE"]["PEM"]
        formats = formats[options["digest"]]
        network = options["network"][0] + options["network"][1:].lower()
        printer = self.director.get_instance("pem_printer", options["header"])

        for i in range(options["keynum"]):
            printer.put(
                [
                    formats[0].format(network, encrypt_outs[i][0]),
                    formats[1].format(encrypt_outs[i][1]),
                    "The encrypted private key block:\n",
                ],
                encode=False,
            )
            printer.put(encrypt_outs[i][2])

        if not options.get("get"):
            po = None
            if options.get("outpath"):
                po = get_next_free_po(options["outpath"])

            printer.print(po=po)
        else:
            results = []
            while not printer.empty():
                results.append(printer.get())
            return results
        return None

    def _print_create_qr(self, options: Options, encrypt_outs: List[Any]) -> Any:
        formats = FORMATS["CREATE"]["QR"][0]
        network = options["network"][0] + options["network"][1:].lower()
        plain_printer = self.director.get_instance("plain_printer")
        qr_printer = self.director.get_instance("qr_printer")

        for i in range(options["keynum"]):
            plain_printer.put(formats.format(options["network"], encrypt_outs[i][0]))
            qr_printer.put(encrypt_outs[i][0].encode("ascii"), encode=False)
            if options["digest"]:
                qr_printer.put(encrypt_outs[i][1])
                plain_printer.put(
                    encrypt_outs[i][1],
                )
            qr_printer.put(encrypt_outs[i][2])

        if not options.get("get"):
            qr_printer.print(po=options["outpath"])
            plain_printer.print()
        else:
            result = []
            for i in range(options["keynum"]):
                results.append(plain_printer.get())
                results.append(qr_printer.get())
            return results
        return None

    def _print_reveal_plain(self, options: Options, decrypt_outs: List[Any]) -> Any:
        formats = FORMATS["REVEAL"]
        printer = self.director.get_instance("plain_printer")

        printer.put(
            [
                formats.format(plaintext_pk.get_secret_value().hex())
                for plaintext_pk in decrypt_outs
            ]
        )

        if not options.get("get"):
            po = None
            if options["outpath"]:
                po = get_next_free_po(options["outpath"])
            printer.print(po=po)
        else:
            result = []
            for i in range(options["keynum"]):
                results.append(printer.get())
            return results
        return None


def get_eth_keys(director: PreDirector):
    return EthKeys(director)


# And now this can be called from top level

PreDirector.register_builder("ethereum", get_eth_keys)
