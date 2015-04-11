FNAME=ncnh
BIB=references.bib
CSL=evolutionary-ecology-research.csl
#CSL=springer-basic-author-date-no-et-al.csl
FLAGS=--smart --from markdown+autolink_bare_uris+ascii_identifiers+implicit_figures+header_attributes+table_captions --filter pandoc-eqnos --filter pandoc-fignos --filter /usr/local/bin/pandoc-citeproc --highlight-style tango --bibliography $(BIB) --csl $(CSL) --latex-engine=xelatex

draft:
	cat [0-1]*md | pandoc -H draft.sty $(FLAGS) --output draft_$(FNAME)_$(shell date +'%Y%m%d').pdf

draft_doc:
	cat [0-1]*md | pandoc -H draft.sty $(FLAGS) --output draft_$(FNAME)_$(shell date +'%Y%m%d').docx

abstract: 01_abstract.md
	pandoc 01_abstract.md -H draft.sty $(FLAGS) --output draft_abstract_$(shell date +'%Y%m%d').pdf

intro: 02_introduction.md references.bib
	pandoc 02_introduction.md -H draft.sty $(FLAGS) --output draft_introduction_$(shell date +'%Y%m%d').pdf

methods: 03_methods.md 09_tables.md references.bib
	cat 03_methods.md 09_tables.md newpage.sty | pandoc -H draft.sty $(FLAGS) --output draft_methods_$(shell date +'%Y%m%d').pdf

results: 04_results.md 08_figures.md references.bib
	cat 04_results.md 08_figures.md newpage.sty | pandoc -H draft.sty $(FLAGS) --output draft_results_$(shell date +'%Y%m%d').pdf

discussion: 05_discussion.md references.bib
	cat 05_discussion.md newpage.sty | pandoc -H draft.sty $(FLAGS) --output draft_discussion_$(shell date +'%Y%m%d').pdf

box: 07_box1.md
	cat 07_box1.md newpage.sty | pandoc -H draft.sty $(FLAGS) --output draft_box1_$(shell date +'%Y%m%d').pdf

figures: 08_figures.md
	cat 08_figures.md newpage.sty | pandoc -H draft.sty $(FLAGS) --output draft_figures_$(shell date +'%Y%m%d').pdf

latest:
	@cat [0-1]*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.pdf
	@cat [0-1]*md | pandoc -H draft.sty $(FLAGS) --output $(FNAME)-latest.docx


clean:                                                                          
	    rm -f $(FNAME).pdf $(FNAME).tex $(FNAME).docx draft_*.pdf
