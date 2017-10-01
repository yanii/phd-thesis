#!/bin/bash
qpdf --qdf $1 - | python strippagegroups.py | fix-qdf >/tmp/tmp.pdf
