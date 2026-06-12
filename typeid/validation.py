from typeid import base32
from typeid.errors import PrefixValidationException


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
    # The codec owns suffix validity (see docs/adr/0001); decoding is validation.
    base32.decode(suffix)
