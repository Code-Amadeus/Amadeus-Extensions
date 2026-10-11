# Theme contract v0

Status: **provisional**. Contract identifier: `amadeus.ui.theme/v0`.
The local P1/P2 Host implementation and its acceptance evidence are reviewed
separately; this document does not claim stable conformance.

A theme is data. It does not execute code, request Host capabilities, inject
stylesheets or alter the Host's base component identity. `base` selects the
Host's `classic` or `wallpaper-slice` styling; the qualified extension selection
is recorded separately. Title-bar style and `colorScheme` follow that base.

`tokens` override only the Host's published CSS-variable allowlist. Status
colors (`--danger*`, `--warning*`, `--success*`) are reserved. Colors accept hex,
rgb/rgba or hsl/hsla literals; fonts reference installed system families only.
URLs, variables, declarations, comments and executable CSS are rejected. The
Host validates and renders the same final palette. Normal text must retain
contrast of at least 4.5 and muted text at least 3 on its actual surfaces.

An optional `background` supplies a package-relative PNG, JPEG or WebP image,
`fit` (`cover` or `contain`) and black-overlay `dim` from 0 to 1. The Host checks
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
