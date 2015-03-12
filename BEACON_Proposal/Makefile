title = bdc-NCNH-beacon-2015

pdf: proposal.md references.bib nature.csl
	pandoc proposal.md -H tweaks.sty --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

notweak: proposal.md references.bib nature.csl
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

draft: proposal.md references.bib nature.csl
	pandoc proposal.md -H draft.sty --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

tex: proposal.md references.bib nature.csl
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).tex --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --standalone

doc: proposal.md references.bib nature.csl
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).docx --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

clean:
	rm -f $(title).pdf $(title).tex $(title).docx
