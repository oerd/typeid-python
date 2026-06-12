import pytest

from typeid.base32 import decode
from typeid.base32 import encode
from typeid.errors import SuffixValidationException


def test_encode_decode_roundtrip() -> None:
    original_data = bytes(range(16))

    encoded_data = encode(original_data)

    assert encoded_data == "00041061050r3gg28a1c60t3gf"
    assert decode(encoded_data) == original_data


def test_encode_rejects_wrong_length() -> None:
    with pytest.raises(ValueError, match="Expected 16 bytes"):
        encode(bytes(15))


def test_decode_rejects_character_outside_alphabet() -> None:
    # "u" is not in the base32 alphabet; one bad character must be enough.
    with pytest.raises(SuffixValidationException):
        decode("01h455vb4pex5vsknk084sn0u2")


def test_decode_rejects_uppercase() -> None:
    # The spec requires strictly lowercase suffixes; no Crockford case-leniency.
    with pytest.raises(SuffixValidationException):
        decode("0123456789ABCDEFGHJKMNPQRS")


def test_decode_rejects_wrong_length() -> None:
    with pytest.raises(SuffixValidationException):
        decode("01h455vb4pex5vsknk084sn02")


def test_decode_rejects_overflow() -> None:
    # First character above "7" would overflow 128 bits.
    with pytest.raises(SuffixValidationException):
        decode("8zzzzzzzzzzzzzzzzzzzzzzzzz")


def test_decode_rejects_non_ascii() -> None:
    with pytest.raises(SuffixValidationException):
        decode("01h455vb4pex5vsknk084sn02β")
