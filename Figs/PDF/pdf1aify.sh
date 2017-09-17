#!/bin/sh
# Embed fonts and make sure version of pdfs are 1.4
for file in *.pdf; do
	gs -q -dColorConversionStrategy=/LeaveColorUnchanged, -dDownsampleMonoImages=false -dDownsampleGrayImages=false -dDownsampleColorImages=false -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -dPDFA -dCompatibilityLevel=1.4 -sDEVICE=pdfwrite -sOutputFile=/tmp/${file} ${file} && mv /tmp/${file} .
done
