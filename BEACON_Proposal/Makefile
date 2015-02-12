title = bdc-NCNH-beacon-2015

pdf: proposal.md references.bib nature.csl
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures --output $(title).pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

doc: proposal.md references.bib nature.csl
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures --output $(title).docx --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

clean:
	rm -f $(title).pdf $(title).docx
