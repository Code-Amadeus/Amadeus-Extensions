# Theme contract v0

Status: **provisional**. Contract identifier: `amadeus.ui.theme/v0`.
The local P1/P2 Host implementation and its acceptance evidence are reviewed
separately; this document does not claim stable conformance.

A theme is data. It does not execute code, request Host capabilities, inject
stylesheets or alter the Host's base component identity. `base` selects the
Host's `classic` or `wallpaper-slice` styling; the qualified extension selection
is recorded separately. Title-bar style and `colorScheme` follow that base.

`tokens` override only the 25 names in the canonical
[theme token allowlist](../../schemas/theme-tokens.v0.json). Host tooling generates
its token names from a pinned copy of this file; adding an internal CSS variable
does not automatically expose it to packages. Status
colors (`--danger*`, `--warning*`, `--success*`) are reserved. Colors accept hex,
rgb/rgba or hsl/hsla literals; fonts reference installed system families only.
Functional literals use either comma-separated components (optional fourth alpha)
or three space-separated components followed by optional `/ alpha`. The forms
cannot be mixed; legacy comma RGB components are all numbers or all percentages.
Shared accepted/rejected cases live in `tests/fixtures/theme-color-literals.json`.
URLs, variables, declarations, comments and executable CSS are rejected. The
reference validator checks the allowlist, literal syntax/ranges, single-family
font syntax, contained image paths, size and file signatures. Installed fonts,
full native image decoding and rendered palette validation remain Host checks.
The Host validates and renders the same final palette. Normal text must retain
contrast of at least 4.5 and muted/faint text at least 3 on its actual surfaces.
Status and accent foreground text must also be checked on the surfaces where
it is displayed. Palettes keep the light/dark identity of their base; surface
colors are opaque to bound nested compositing. The Host provides a native or
otherwise theme-independent way to restore a built-in theme, even if a selected
font renders unreadable glyphs.

An optional `background` supplies a package-relative PNG or JPEG image,
WebP is excluded from v0 because the current native Host decoder cannot validate
it. Renaming a WebP file does not make it a PNG/JPEG. `fit` (`cover` or `contain`) and black-overlay `dim` from 0 to 1. The Host checks
decoded dimensions (each at most 4096), size (8 MiB), path containment and absence
of links. Image contrast is evaluated over the entire possible luminance range
after dim/surface compositing, including interior minima. Looking only at a
black and white endpoint is insufficient when text lies between them.
Host-validated image bytes cross into the renderer; package filesystem URLs do
not. Old object URLs/styles are released on switching, disabling or removal.

New `runtime.kind=none` wheels cannot declare dependencies; the inspected package
resources are extracted without a virtual environment, pip or package imports.
The existing wheel inspection and ownership rules still apply.

Pure frontend packages apply immediately. If either the old or new package has
backend contributions, its version/configuration changes apply together after
backend restart. Frontend resources use the actual loaded snapshot, never new
desired metadata with old code. Disabling/removing closes frontend admission
immediately; the interface must still disclose a backend awaiting shutdown.

When a selected theme becomes unavailable, keep its saved identity and report
the reason while falling back to its last verified base (otherwise the Host
default). Reinstalling never silently enables a package. Resource cleanup follows
actual references and preserves retryable ownership after a deletion failure.
