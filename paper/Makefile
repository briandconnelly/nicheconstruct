FNAME=ncnh
FLAGS=--from markdown+autolink_bare_uris+ascii_identifiers+tex_math_single_backslash+implicit_figures+header_attributes --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --latex-engine=xelatex

draft:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)_draft_$(shell date +'%Y%m%d').pdf

draft_doc:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)_draft_$(shell date +'%Y%m%d').docx

clean:                                                                          
	    rm -f $(FNAME)*.pdf $(FNAME)*.tex $(FNAME)*.docx 
