FNAME=ncnh
BIB=references.bib
CSL=evolutionary-ecology-research.csl
#CSL=springer-basic-author-date-no-et-al.csl
FLAGS=--smart --from markdown+autolink_bare_uris+ascii_identifiers+implicit_figures+header_attributes+table_captions --filter /usr/local/bin/pandoc-citeproc --filter pandoc-eqnos --highlight-style tango --bibliography $(BIB) --csl $(CSL) --latex-engine=xelatex

draft:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output draft_$(FNAME)_$(shell date +'%Y%m%d').pdf

draft_doc:
	cat 0*md | pandoc -H draft.sty $(FLAGS) --output draft_$(FNAME)_$(shell date +'%Y%m%d').docx

intro: 01_introduction.md references.bib
	pandoc 01_introduction.md -H draft.sty $(FLAGS) --output draft_introduction_$(shell date +'%Y%m%d').pdf

methods: 02_methods.md references.bib
	pandoc 02_methods.md -H draft.sty $(FLAGS) --output draft_methods_$(shell date +'%Y%m%d').pdf

latest:
	@cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.pdf
	@cat 0*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.docx


clean:                                                                          
	    rm -f $(FNAME)*.pdf $(FNAME)*.tex $(FNAME)*.docx 
