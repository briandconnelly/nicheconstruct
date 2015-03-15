all:
	pdflatex biosketch-connelly
	bibtex biosketch-connelly
	pdflatex biosketch-connelly
	pdflatex biosketch-connelly

xelatex:
	xelatex biosketch-connelly
	bibtex biosketch-connelly
	xelatex biosketch-connelly
	xelatex biosketch-connelly

proof:
	@echo "Weasel words: "
	@echo "---------------------------------------------------------"
	@sh ../bin/weasel.sh *.tex
	@echo
	@echo "Duplicates:"
	@echo "---------------------------------------------------------"
	@../bin/dups.pl *.tex
	@echo
	@echo "Passive:"
	@echo "---------------------------------------------------------"
	@sh ../bin/passive.sh *.tex

clean:
	rm -f biosketch-connelly.log biosketch-connelly.dvi biosketch-connelly.aux biosketch-connelly.pdf biosketch-connelly.ps biosketch-connelly.blg biosketch-connelly.out biosketch-connelly.bbl
