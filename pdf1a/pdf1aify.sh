#!/bin/sh
gs -dPDFA=1 -dBATCH -dNOPAUSE -dNOOUTERSAVE -dUseCIEColor -sColorConversionStrategy=/RGB -sOutputICCProfile=default.icc -sDEVICE=pdfwrite -dPDFACompatibilityPolicy=1 -sOutputFile=`basename ${1} .pdf`-PDF1A.pdf "pdf1a/PDFA_def.ps" $1
