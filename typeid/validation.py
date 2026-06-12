from typeid import base32
from typeid.constants import SUFFIX_LEN
from typeid.errors import PrefixValidationException
from typeid.errors import SuffixValidationException


def validate_prefix(prefix: str) -> None:
    # See https://github.com/jetify-com/typeid/tree/main/spec
    if prefix is None:
        raise PrefixValidationException("No prefix provided.")

    if prefix[0] == "_" or prefix[-1] == "_":
        raise PrefixValidationException("Prefix cannot start or end with '_'.")

    if len(prefix) > 63:
        raise PrefixValidationException("Prefix cannot be longer than 63 characters.")

    for char in prefix:
        if not ("a" <= char <= "z" or char == "_"):
            raise PrefixValidationException("Prefix can only contain ASCII letters 'a-z' or '_'.")


def validate_suffix(suffix: str) -> None:
    if (
        len(suffix) != SUFFIX_LEN
        or suffix == ""
        or " " in suffix
        or (not suffix.isdigit() and not suffix.islower())
        or any([symbol not in base32.ALPHABET for symbol in suffix])
        or suffix[0] > "7"
    ):
        raise SuffixValidationException(f"Invalid suffix: {suffix}.")
    try:
        base32.decode(suffix)
    except Exception as exc:
        raise SuffixValidationException(f"Invalid suffix: {suffix}.") from exc
