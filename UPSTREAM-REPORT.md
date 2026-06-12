# Upstream sync report: `akhundMurad/typeid-python` vs our fork

**Date:** 2026-06-12 · **Fork point:** `f66753d` ("fix: clean up whitespaces", v0.3.2) ·
**Missing commits:** 114 (upstream `main`) · **Upstream version:** 0.3.9 ·
**Diff size:** 96 files, +7,417 / −956

## TL;DR

Upstream has been very active since we forked. Three things dominate: the base32
codec was **rewritten in Rust** (maturin build, no Python fallback), the package
was **reorganized into `typeid/core/`, `typeid/codecs/`, `typeid/cli/`,
`typeid/integrations/`** (with compat shims at the old paths), and several
genuinely useful **features** landed (Pydantic v2 field, `typeid explain` CLI,
TypeID factories, timestamp properties). Two of our four fork-side changes were
independently duplicated upstream; the other two collide with or are superseded
by upstream's direction. The decision is less "which commits to take" and more
"do we want to follow upstream's Rust-native architecture or stay a simple
pure-Python fork."

---

## 1. Rust-backed base32 codec (architectural, breaking for us)

- `typeid/codecs/base32.py` is now a thin wrapper over `typeid._base32`, a
  CPython extension built from `rust-base32/` via **maturin** (`build-backend =
  "maturin"`). There is **no Python fallback** — building/installing the fork
  would require a Rust toolchain everywhere (their CI installs it on every
  runner; they ship macOS/Linux universal and linux/arm64 wheels to compensate).
- A `bench/` suite with committed JSON results justifies the move
  (`pytest-benchmark`, before/after Rust).
- The old buggy pure-Python decoder (the `and`-instead-of-`or` chain we fixed in
  our PR #6) was **deleted**, not fixed — superseded by Rust.
- Convergent thinking worth noting: their codec docstring says almost exactly
  what our ADR 0001 says — *"It is **not** a general-purpose Base32 encoder"*,
  strictly 16 bytes / 26 chars, lowercase only, no Crockford aliases.
- Where they differ from our PR #6 design: the Rust codec raises **untyped
  `RuntimeError`s**, and `typeid/core/validation.py` still **duplicates the
  validity rules in front of the decoder** (`validate_suffix_and_decode` checks
  length / spaces / `islower` / alphabet / overflow, *then* decodes). Their
  commit `5604952` "fix: validation didn't include all cases" actually
  *re-expanded* the duplicated check chain — the exact two-copies-of-the-rules
  pattern our PR #6 eliminated. If we adopt upstream, that design critique
  survives and could be contributed back.

## 2. Package reorganization

New layout: `typeid/core/{typeid,validation,parsing,factory,errors,constants}.py`,
`typeid/codecs/base32.py`, `typeid/cli/main.py`, `typeid/integrations/pydantic/v2.py`.
Old import paths (`typeid.base32`, `typeid.validation`, `typeid.constants`, …)
remain as documented **compatibility shims**, so downstream imports keep working.
`typeid/__init__.py` now also exports `from_string`, `from_uuid`,
`get_prefix_and_suffix`, and the factory helpers.

## 3. New features

| Feature | Commits | Notes |
|---|---|---|
| Pydantic v2 integration | `40294fe`, `baa8db5`, `f97bc29` | `TypeIDField["user"]` with core-schema validation, `Literal` prefix support, FastAPI/OpenAPI JSON-schema fix. Optional dep. |
| `typeid explain` CLI | `72eab0c`, `b200efc` | Human/machine-readable introspection of a TypeID, optional JSON/YAML schema lookup; CLI moved to a package with `cli`/`yaml` extras. |
| TypeID factories | `be16684` | `TypeIDFactory`, `typeid_factory(prefix)`, `cached_typeid_factory(prefix)` — reusable, cached generators. |
| Timestamp properties | `0525ea2`, `5681023` | `timestamp_ms` / `created_at` (now `Optional[datetime]`) on `TypeID`. |
| Other UUID versions | `a4edf6c` | `TypeID` no longer assumes UUIDv7; timestamp properties return `None` when not applicable. |
| Typed prefixes | `7af0647`, `13b9792` | `TypeID(Generic[PrefixT])` — prefix can be a `Literal` type for static checking. |
| Smaller API niceties | `d132255`, `8c24cf9` | Executable `repr()` (`TypeID.from_string(...)`), `from_uuid` accepts stdlib `uuid.UUID`. |

## 4. Packaging, CI, docs

- **uv migration** (`d166278`, `fb63be2`) — duplicates our PR #2; both sides now
  use uv + `uuid-utils`, so this merges easily in spirit but conflicts textually.
- **PyPI/TestPyPI publish pipelines**, tag-triggered releases, multi-platform
  wheel builds (the newest commit, `e4f2926`, adds linux/arm64).
- **Full mkdocs-material docs site** (`d9aa4c5`, `78d3442`) with API reference,
  framework-integration guides, performance section.
- **pre-commit hooks**, Makefile cleanup, black (line-length 119) + ruff —
  their lint config differs from our PR #3 ruff-only setup.
- Python floor raised to **3.10**; classifiers through 3.14.

## 5. Collision map with our fork-only work

| Ours | Status vs upstream |
|---|---|
| PR #1 — `validate_prefix` rewrite | Upstream has its own equivalent in `core/validation.py`; behavior overlaps, code differs. Low-value conflict. |
| PR #2 — uv + uuid-utils | Independently done upstream. Ours is redundant after a sync. |
| PR #3 — ruff rules trim | Upstream kept black + its own ruff config. Cosmetic conflict; pick one. |
| PR #6 — validity-owning base32 codec (+ CONTEXT.md, ADR 0001) | **Superseded mechanically** by the Rust codec (the bug it fixed no longer exists upstream), but **not superseded conceptually**: upstream still duplicates validation outside the codec and throws untyped errors. The docs (CONTEXT.md, ADR) carry over regardless. |

## 6. Options

1. **Re-sync onto upstream** (recommended *if* we want the features and can
   accept the Rust/maturin build): reset fork `main` to upstream `main`, then
   replay the little that's genuinely ours — CONTEXT.md, docs/adr/, any local
   conventions. Our PRs #1–#3 dissolve; PR #6's error-contract design becomes a
   candidate contribution *to* upstream instead.
2. **Cherry-pick features, skip the Rust core**: Pydantic field, `explain`,
   factories, and timestamp properties are mostly pure-Python and portable, but
   they're written against the `typeid/core/` layout — porting means hand-editing
   imports on every pick and forfeiting future easy syncs. Ongoing tax.
3. **Stay diverged**: keep the fork as a minimal pure-Python TypeID with our
   single-home validation design. Cheapest now; we permanently forgo upstream's
   features, wheels, and fixes.

The real fork-in-the-road is the **Rust dependency**. Everything else (features,
docs, CI) comes along almost for free once that's accepted — and our remaining
delta shrinks to documentation and design taste.
