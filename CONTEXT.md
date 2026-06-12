# CONTEXT.md

Domain glossary for typeid-python. Terms only — no implementation details.

## TypeID

A type-safe, K-sortable, globally unique identifier, rendered as
`prefix_suffix` (e.g. `user_01h455vb4pex5vsknk084sn02q`) or as a bare
suffix when there is no prefix. Defined by the
[TypeID spec](https://github.com/jetify-com/typeid/tree/main/spec).

## Prefix

The type name part of a TypeID. At most 63 characters, lowercase ASCII
letters and underscores only, must not start or end with an underscore.
Optional — a TypeID without a prefix is just a suffix.

## Suffix

The identifier part of a TypeID: a 26-character base32 encoding of a
128-bit UUID (UUIDv7 by default). K-sortable — lexicographic order of
suffixes matches creation-time order.

## Suffix validity

A suffix is valid if and only if it can be decoded: exactly 26
characters, every character drawn from the Alphabet, and the first
character no greater than `7` (the overflow rule — a 26-character
base32 string can express more than 128 bits, so leading characters
above `7` would overflow the UUID).

## Alphabet

The lowercase Crockford-style base32 alphabet
`0123456789abcdefghjkmnpqrstvwxyz` — digits and lowercase letters
excluding `i`, `l`, `o`, `u` (which are easily confused with `1` and `0`).
