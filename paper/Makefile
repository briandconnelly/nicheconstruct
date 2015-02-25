title = outline

outline: outline.md references.bib evolutionary-ecology-research.csl
	pandoc outline.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --number-section
	pandoc outline.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --output $(title).docx --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

clean:
	rm -f $(title).pdf $(title).tex $(title).docx
