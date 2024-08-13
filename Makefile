DATA?=data.json

all: staging/main.tex
	pdflatex staging/main.tex
	pdflatex staging/main.tex
	rm -Rf staging

staging/main.tex: ${DATA} ./src/1_makepage.py
	mkdir -p staging
	cp src/0_head.tex staging/main.tex
	./src/1_makepage.py ${DATA} >> staging/main.tex
	cat src/2_tail.tex >> staging/main.tex
