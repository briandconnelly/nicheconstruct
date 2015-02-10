#!/bin/sh

#pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash-implicit_figures --output PROP.pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --bibliography references.bib

pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash-implicit_figures --output PROP.pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango
