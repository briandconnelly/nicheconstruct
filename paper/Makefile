FNAME=ncnh
BIB=references.bib
CSL=evolutionary-ecology-research.csl
#CSL=springer-basic-author-date-no-et-al.csl
FLAGS=--smart --from markdown+autolink_bare_uris+ascii_identifiers+implicit_figures+header_attributes+table_captions --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --bibliography $(BIB) --csl $(CSL) --latex-engine=xelatex

draft:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)_draft_$(shell date +'%Y%m%d').pdf

draft_doc:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)_draft_$(shell date +'%Y%m%d').docx

methods: 02_methods.md references.bib
	pandoc 02_methods.md -H draft.sty $(FLAGS) --output methods_draft_$(shell date +'%Y%m%d').pdf

latest:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.pdf
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.docx


clean:                                                                          
	    rm -f $(FNAME)*.pdf $(FNAME)*.tex $(FNAME)*.docx 
