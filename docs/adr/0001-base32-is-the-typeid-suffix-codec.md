# base32 is the TypeID suffix codec, not a general-purpose library

`typeid/base32.py` deliberately speaks the TypeID domain: `decode` raises
`SuffixValidationException` on any invalid suffix (wrong length, character
outside the Alphabet, overflow rule violated), and the interface is
`encode(bytes) -> str` / `decode(str) -> bytes`. We considered keeping the
module domain-neutral with its own error type and a mapping layer in
`typeid/validation.py`, and rejected it: this module exists only to encode
TypeID suffixes, and the neutral design is what allowed the validity rules
to be duplicated — with the two copies disagreeing (the in-codec check was
broken while the duplicate in `validation.py` papered over it, letting the
CLI decode garbage silently). One copy of suffix validity lives in the
codec; everything else delegates to it.
