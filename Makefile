DATA?=testdata

all: staging/main.tex
	pdflatex staging/main.tex
	pdflatex staging/main.tex
	rm -Rf staging

staging/main.tex:
	mkdir -p staging
	./main.py ${DATA}/* > staging/main.tex