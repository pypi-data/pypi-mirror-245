# postpone evaluation of annotations
from __future__ import annotations

import abc

from typing import Optional, Any, Type, Union, List, AnyStr

from .base import Super, AdHoc

from .utils import get_next_free_po

from pathlib import Path

from base64 import b64encode, b64decode

from re import sub

from queue import Queue

from segno import make_qr, QRCode


def _write(data: AnyStr, *args, **kwargs) -> None:
    po = kwargs.pop("po", None)

    if po:
        mode = "a" if po.exists() else "x"
        kwargs.update({"file": po.open(mode=mode)})

    print(data, *args, **kwargs)

    if po:
        kwargs["file"].close()


def _write_qr(
    qr: QRCode,
    **kwargs,
) -> None:
    po = kwargs.pop("po", None)

    if not po:
        raise ValueError("QRCodeWriter._write_qr: a path object is required!")

    if po.suffix == "":
        po = po.with_suffix(".png")

    po = get_next_free_po(po)

    qr.save(
        po.absolute(),
        dark=kwargs.get("dark") or "black",
        light=kwargs.get("light") or "white",
        scale=kwargs.get("scale") or 20,
        **kwargs,
    )


class Writer(abc.ABC):
    """Derived classes of this base class should implement
    logic for essentially writing data to some buffer,
    preparing that data for writing, and also decoding it
    when reading it out of some buffer.

    Encoding and decoding thus, is not to be taken in the
    str and bytes sense, of encoding to bytes and decoding
    from bytes to str, and instead in the sense of encoding
    arbitrary data in some way, and decoding it back to some
    format.

    We specify that each function has to at least take
    one data argument. Everything further is laissez faire
    including narrowing and expanding arguments in derived
    classes to enforce behaviour.
    """

    @abc.abstractmethod
    def write(self, data: Any, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def encode(self, data: Any, *args, **kwargs) -> Any:
        pass

    @abc.abstractmethod
    def decode(self, data: Any, *args, **kwargs) -> Any:
        pass


class PlainWriter(Writer):
    def write(self, data: AnyStr, *args, **kwargs) -> None:
        _write(data, *args, **kwargs)

    def encode(self, data: Any) -> Any:
        return data

    def decode(self, data: Any) -> Any:
        return data


class HexWriter(Writer):
    def write(self, data: AnyStr, *args, **kwargs) -> None:
        _write(data, *args, **kwargs)

    def encode(self, data: bytes) -> str:
        return data.hex()

    def decode(self, data: str) -> bytes:
        return bytes.fromhex(data)


class Base64Writer(Writer):
    character_encoding: str = "ascii"

    def write(self, data: AnyStr, *args, **kwargs) -> None:
        _write(data, *args, **kwargs)

    def encode(self, data: bytes) -> str:
        return b64encode(data).decode(self.character_encoding)

    def decode(self, data: str) -> bytes:
        return b64decode(data.encode(self.character_encoding))


class FormatWriter(Writer):
    format_template_base: str
    decode_template_pattern: str
    format_template: str = None
    character_encoding: str = "ascii"

    def __format_guard(self) -> None:
        if self.format_template is None:
            raise ValueError("Format template has not been set, can't en- or decode!")

    def write(self, data: AnyStr, *args, **kwargs) -> None:
        _write(data, *args, **kwargs)

    @abc.abstractmethod
    def encode(self, data: Any, *args, **kwargs) -> Any:
        self.__format_guard()

    @abc.abstractmethod
    def decode(self, data: Any, *args, **kwargs) -> Any:
        self.__format_guard()

    @abc.abstractmethod
    def set_format(self, inserts: List[str]) -> str:
        pass


class PEMWriter(FormatWriter):
    format_template_base: str = "-----BEGIN {}-----\n\n{}\n\n-----END {}-----\n"
    decode_template_pattern: str = "-+(BEGIN|END) [ A-Z]+-+"

    @Super.PreCall
    def encode(self, data: bytes) -> str:
        encoded64: str = b64encode(data).decode(self.character_encoding)
        return self.format_template.format(
            "\n".join(
                [
                    encoded64[index * 64 : (index + 1) * 64]
                    for index in range(0, int(len(encoded64) / 64) + 1)
                ]
            )
        )

    @Super.PreCall
    def decode(self, data: str) -> bytes:
        return b64decode(
            "".join(sub(self.decode_template_pattern, "", data).strip()).encode(
                self.character_encoding
            )
        )

    def set_format(self, inserts: List[str]) -> None:
        self.format_template = self.format_template_base.format(
            inserts[0], "{}", inserts[1]
        )


class QRCodeWriter(Base64Writer):
    def write(self, data: AnyStr, *args, **kwargs) -> None:
        _write_qr(make_qr(data, error=kwargs.get("error") or "H", *args), **kwargs)

    def encode(self, data: bytes, **kwargs) -> str:
        return super().encode(data)

    def decode(self, data: str, **kwargs) -> bytes:
        return super().decode(data)


class Printer(Queue):
    _writer_type: Type[Writer]

    writer: Writer

    def __class_getitem__(cls: Type[Self], writer_type: Type[Writer]):
        class ConcretePrinterType(cls):
            pass

        ConcretePrinterType._writer_type = writer_type
        return ConcretePrinterType

    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self.writer = self._writer_type()

    def print(self, *args, **kwargs) -> None:
        while not self.empty():
            self.writer.write(self.get(), *args, **kwargs)

    @AdHoc.ListMorph(0)
    def put(
        self,
        item: Any,
        encode: bool = True,
        block: bool = True,
        timeout: Optional[float] = None,
    ) -> None:
        item = self.writer.encode(item) if encode else item
        super().put(item, block=block, timeout=timeout)
