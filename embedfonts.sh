#!/bin/sh
# from https://www.karlrupp.net/2016/01/embed-all-fonts-in-pdfs-latex-pdflatex/
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dEmbedAllFonts=true -sOutputFile=thesis_embed.pdf -f thesis.pdf
