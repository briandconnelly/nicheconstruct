
pdf:
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash-implicit_figures --output PROP.pdf --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

doc:
	pandoc proposal.md --from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash-implicit_figures --output PROP.docx --filter /usr/local/bin/pandoc-citeproc --highlight-style tango

clean:
	rm -f PROP.pdf PROP.docx
