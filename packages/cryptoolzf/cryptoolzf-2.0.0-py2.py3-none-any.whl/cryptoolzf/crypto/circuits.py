import abc

from typing import List, Union, Optional, Type, TypeVar, Generic

# Circuits are Base Models because circuit data is important
from pydantic import BaseModel, validator
from pydantic import Field, SecretBytes, SecretField

from pydantic.generics import GenericModel
from pydantic.errors import MissingError

from secrets import token_bytes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as pbdkf2
from cryptography.hazmat.primitives.ciphers.aead import AESGCM as aesgcm
from cryptography.hazmat.primitives.hashes import (
    Hash,
    SHA3_512 as sha3_512,
    BLAKE2b as blake2b,
)

from cryptography.exceptions import InvalidTag

from .exceptions import WrongDecryptionInputs

# Bases


class CircuitInsBase(BaseModel):
    class Config:
        # Validate field defaults
        validate_all = True
        # Validate fields on assignment
        validate_assignment = True


class CircuitOutsBase(BaseModel):
    class Config:
        # Fields are immutable
        allow_mutation = False


CircuitInsType = TypeVar("InType", bound=CircuitInsBase)
CircuitOutsType = TypeVar("OutType", bound=CircuitOutsBase)


class CircuitLike(GenericModel, Generic[CircuitInsType, CircuitOutsType], abc.ABC):
    ins: CircuitInsType
    outs: Optional[CircuitOutsType] = None

    @abc.abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs) -> CircuitOutsType:
        if len(kwargs) != 0:
            self.ins = type(self.ins)(**kwargs)
        self.outs = type(self).compute_outs(self.ins)
        return self.outs

    @abc.abstractclassmethod
    def validate_circuit_ins(cls, ins: CircuitInsType) -> CircuitInsType:
        pass

    @abc.abstractclassmethod
    def compute_outs(cls, ins: CircuitInsType) -> CircuitOutsType:
        pass

    class Config:
        # Validate field defaults
        validate_all = True
        # Validate fields on assignment
        validate_assignment = True


SecretType = TypeVar("SecretType", bound=SecretField)

InternalInput = Union
ExternalInput = Union[SecretType, None]
PublicOutput = Union
SecretOutput = Union[SecretType, None]

# BLAKE2b


class InsBLAKE2B(BaseModel):
    blake2b_data: ExternalInput[List[SecretBytes]] = None
    # Set to True to get intermediate digests
    blake2b_intermediate: InternalInput[bool] = False
    # Currently only 64 supported
    blake2b_digest_size: InternalInput[int] = 64


class OutsBLAKE2B(BaseModel):
    blake2b_digests: PublicOutput[List[bytes]] = []


class HashBLAKE2B(CircuitLike[InsBLAKE2B, OutsBLAKE2B]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsBLAKE2B(**kwargs))

    @validator("ins")
    def validate_circuit_ins(cls, ins: InsBLAKE2B) -> InsBLAKE2B:
        if ins.blake2b_digest_size != 64:
            raise ValueError(
                "HashBLAKE2B.validate_circuit_ins: digest size may currently only be 64!"
            )
        return ins

    @classmethod
    def compute_outs(cls, ins: InsBLAKE2B) -> OutsBLAKE2B:
        if ins.blake2b_data is None or len(ins.blake2b_data) == 0:
            raise ValueError("HashBLAKE2B.compute_outs: There is not data to hash!")

        digests = []
        hash_fn = Hash(blake2b(64))

        if ins.blake2b_intermediate:
            for bytes_data in ins.blake2b_data:
                digests.append(hash_fn.update(bytes_data).copy().finalize())
        else:
            for bytes_data in ins.blake2b_data:
                hash_fn.update(bytes_data)

        digests.append(hash_fn.finalize())

        return OutsBLAKE2B(blake2b_digests=digests)


# PBDKF2HMAC

pbdkf2_accepted_digests = {
    "sha3_512": sha3_512,
}

pbdkf2_max_key_size_bytes = {
    "sha3_512": (2**32 - 1) * pbdkf2_accepted_digests["sha3_512"].digest_size
}


class InsPBDKF2(BaseModel):
    pbdkf2_passphrase: ExternalInput[SecretBytes] = None
    pbdkf2_hash_fn_name: InternalInput[str] = "sha3_512"
    pbdkf2_key_size_bytes: InternalInput[int] = 32
    pbdkf2_salt: InternalInput[bytes] = Field(default_factory=lambda: token_bytes(32))
    pbdkf2_iterations: InternalInput[int] = 40000
    pbdkf2_salt_size_bytes: InternalInput[int] = 32


class OutsPBDKF2(BaseModel):
    pbdkf2_derived_key: SecretOutput[SecretBytes] = None
    pbdkf2_salt: PublicOutput[bytes] = b""


class InsDerivePBDKF2(CircuitInsBase, InsPBDKF2):
    pass


class OutsDerivePBDKF2(CircuitOutsBase, OutsPBDKF2):
    pass


class DerivePBDKF2(CircuitLike[InsDerivePBDKF2, OutsDerivePBDKF2]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsDerivePBDKF2(**kwargs))

    @validator("ins")
    def validate_circuit_ins(cls, ins: InsDerivePBDKF2) -> InsDerivePBDKF2:
        salt_len = len(ins.pbdkf2_salt)

        # General
        if ins.pbdkf2_hash_fn_name not in pbdkf2_accepted_digests:
            raise ValueError(
                f"DerivePBDKF2.compute_outs: {ins.pbdkf2_hash_fn_name} is not part of this module because it is not recommended, or does not exist."
            )
        if ins.pbdkf2_salt_size_bytes != salt_len:
            raise ValueError(
                "DerivePBDKF2.validate_circuit_ins: Salt size does not correspond to stated size!"
            )

        # Minimums
        if salt_len < 16:
            raise ValueError(
                "DerivePBDKF2.validate_circuit_ins: Salt should be minimum 16 bytes!"
            )
        if ins.pbdkf2_key_size_bytes < 16:
            raise ValueError(
                "DerivePBDKF2.validate_circuit_ins: Key size should be minimum 16 bytes!"
            )
        if ins.pbdkf2_iterations < 10000:
            raise ValueError(
                "DerivePBDKF2.validate_circuit_ins: Iterations should be minimum 10000!"
            )

        # Maximums
        if (
            pbdkf2_max_key_size_bytes[ins.pbdkf2_hash_fn_name]
            < ins.pbdkf2_key_size_bytes
        ):
            raise ValueError(
                "DerivePBDKF2.validate_circuit_ins: derived key size is above maximum allowed according to digest!"
            )

        return ins

    @classmethod
    def compute_outs(cls, ins: InsDerivePBDKF2) -> OutsDerivePBDKF2:
        if ins.pbdkf2_passphrase is None:
            raise ValueError(
                "DerivePBDKF2.compute_outs: A derivation passphrase is necessary!"
            )

        digest = pbdkf2_accepted_digests[ins.pbdkf2_hash_fn_name]

        kdf = pbdkf2(
            digest, ins.pbdkf2_key_size_bytes, ins.pbdkf2_salt, ins.pbdkf2_iterations
        )

        return OutsDerivePBDKF2(
            pbdkf2_derived_key=SecretBytes(
                kdf.derive(ins.pbdkf2_passphrase.get_secret_value())
            ),
            pbdkf2_salt=ins.pbdkf2_salt,
        )


# AESGCM

aesgcm_nonce_max_len = (2**64 - 1) / 8


class InsAESGCM(BaseModel):
    aesgcm_key: ExternalInput[SecretBytes] = None
    aesgcm_plaintext: ExternalInput[SecretBytes] = None
    # IV should be at least 12 bytes, and is usually set to 12 bytes as such
    aesgcm_nonce: InternalInput[bytes] = Field(default_factory=lambda: token_bytes(12))


class OutsAESGCM(BaseModel):
    # For decryption
    aesgcm_key: SecretOutput[SecretBytes] = None
    # The cyphertext has the nonce concatenated
    aesgcm_cyphertext: PublicOutput[bytes] = b""
    # If the nonce is not 12 bytes, set this
    aesgcm_nonce_size_bytes: PublicOutput[int] = 12


class InsEncryptAESGCM(CircuitInsBase, InsAESGCM):
    pass


class OutsEncryptAESGCM(CircuitOutsBase, OutsAESGCM):
    pass


class EncryptAESGCM(CircuitLike[InsEncryptAESGCM, OutsEncryptAESGCM]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsEncryptAESGCM(**kwargs))

    @validator("ins")
    def validate_circuit_ins(cls, ins: InsEncryptAESGCM) -> InsEncryptAESGCM:
        key_len = ins.aesgcm_key and len(ins.aesgcm_key)
        nonce_len = len(ins.aesgcm_nonce)

        # General
        if key_len and key_len % 16 != 0:
            if key_len != 24:
                raise ValueError(
                    f"EncryptAESGCM.validate_circuit_ins: Key must be either 16, 24 or 32 bytes, not {key_len}!"
                )

        # Minimums
        if nonce_len < 12:
            raise ValueError(
                "EncryptAESGCM.validate_circuit_ins: Nonce should be minimum 12 bytes!"
            )

        # Maximums
        if aesgcm_nonce_max_len < nonce_len:
            raise ValueError(
                "EncryptAESGCM.validate_circuit_ins: Nonce exceeds size limit of 2**64 - 1 bits!"
            )

        return ins

    @classmethod
    def compute_outs(cls, ins: InsEncryptAESGCM) -> OutsEncryptAESGCM:
        if ins.aesgcm_key is None:
            raise ValueError(
                "EncryptAESGCM.compute_outs: Cannot encrypt without an AESGCM key!"
            )
        if ins.aesgcm_plaintext is None:
            raise ValueError("EncryptAESGCM.compute_outs: No plaintext to encrypt!")

        return OutsEncryptAESGCM(
            aesgcm_key=None,
            aesgcm_cyphertext=aesgcm(ins.aesgcm_key.get_secret_value()).encrypt(
                ins.aesgcm_nonce, ins.aesgcm_plaintext.get_secret_value(), None
            )
            + ins.aesgcm_nonce,
        )


class InsDecryptAESGCM(CircuitInsBase, OutsAESGCM):
    pass


class OutsDecryptAESGCM(CircuitOutsBase, InsAESGCM):
    pass


class DecryptAESGCM(CircuitLike[InsDecryptAESGCM, OutsDecryptAESGCM]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsDecryptAESGCM(**kwargs))

    @validator("ins")
    def validate_circuit_ins(cls, ins: InsDecryptAESGCM) -> InsDecryptAESGCM:
        return ins

    @classmethod
    def compute_outs(cls, ins: InsDecryptAESGCM) -> OutsDecryptAESGCM:
        if ins.aesgcm_key is None:
            raise ValueError(
                "DecryptAESGCM.compute_outs: Cannot decrypt without an AESGCM key!"
            )
        if ins.aesgcm_cyphertext == b"":
            raise ValueError("DecryptAESGCM.compute_outs: No cyphertext to decrypt!")

        aesgcm_nonce: bytes = ins.aesgcm_cyphertext[-ins.aesgcm_nonce_size_bytes :]

        try:
            return OutsDecryptAESGCM(
                aesgcm_plaintext=aesgcm(ins.aesgcm_key.get_secret_value()).decrypt(
                    aesgcm_nonce,
                    ins.aesgcm_cyphertext[: -ins.aesgcm_nonce_size_bytes],
                    None,
                ),
                aesgcm_nonce=aesgcm_nonce,
            )
        except InvalidTag as ite:
            raise WrongDecryptionInputs(
                "DecryptAESGCM.compute_outs: Decryption inputs are wrong!"
            ) from ite

        raise RuntimeError(
            "DecryptAESGCM.compute_outs: program should have never reached this point!"
        )


# combined


class InsEncryptPBDKF2_AESGCM(CircuitInsBase, InsAESGCM, InsPBDKF2):
    pass


class EncryptPBDKF2_AESGCM(CircuitLike[InsEncryptPBDKF2_AESGCM, OutsEncryptAESGCM]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsEncryptPBDKF2_AESGCM(**kwargs))

    @validator("ins")
    def validate_circuit_ins(
        cls, ins: InsEncryptPBDKF2_AESGCM
    ) -> InsEncryptPBDKF2_AESGCM:
        EncryptAESGCM.validate_circuit_ins(DerivePBDKF2.validate_circuit_ins(ins))
        return ins

    @classmethod
    def compute_outs(cls, ins: InsEncryptPBDKF2_AESGCM) -> OutsEncryptAESGCM:
        if ins.pbdkf2_passphrase is None:
            raise ValueError(
                "EncryptPBDKF2_AESGCM.compute_outs: A derivation passphrase is necessary!"
            )
        if ins.aesgcm_plaintext is None:
            raise ValueError(
                "EncryptPBDKF2_AESGCM.compute_outs: No plaintext to encrypt!"
            )

        pbdkf2_result: OutsPBDKF2 = DerivePBDKF2.compute_outs(ins)

        ins.aesgcm_key = pbdkf2_result.pbdkf2_derived_key

        aesgcm_result: OutsEncryptAESGCM = EncryptAESGCM.compute_outs(ins)

        return OutsEncryptAESGCM(
            aesgcm_key=None,
            aesgcm_cyphertext=aesgcm_result.aesgcm_cyphertext + ins.pbdkf2_salt,
        )


class InsDecryptPBDKF2_AESGCM(CircuitInsBase, OutsAESGCM, InsPBDKF2):
    pass


class DecryptPBDKF2_AESGCM(CircuitLike[InsDecryptPBDKF2_AESGCM, OutsDecryptAESGCM]):
    def __init__(self, **kwargs):
        super().__init__(ins=InsDecryptPBDKF2_AESGCM(**kwargs))

    @validator("ins")
    def validate_circuit_ins(
        cls, ins: InsDecryptPBDKF2_AESGCM
    ) -> InsDecryptPBDKF2_AESGCM:
        DecryptAESGCM.validate_circuit_ins(DerivePBDKF2.validate_circuit_ins(ins))
        return ins

    @classmethod
    def compute_outs(cls, ins: InsDecryptPBDKF2_AESGCM) -> OutsDecryptAESGCM:
        if ins.pbdkf2_passphrase is None:
            raise ValueError(
                "DecryptPBDKF2_AESGCM.compute_outs: A passphrase for key derivation is necessary!"
            )

        ins.pbdkf2_salt = ins.aesgcm_cyphertext[-ins.pbdkf2_salt_size_bytes :]

        pbdkf2_result: OutsPBDKF2 = DerivePBDKF2.compute_outs(ins)

        return DecryptAESGCM.compute_outs(
            InsDecryptAESGCM(
                aesgcm_key=pbdkf2_result.pbdkf2_derived_key,
                aesgcm_cyphertext=ins.aesgcm_cyphertext[: -ins.pbdkf2_salt_size_bytes],
            )
        )
