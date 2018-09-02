#!/bin/bash

if [ $# -ne 1 ] 
then
    echo "USAGE: This script needs exactly one paramter: the path to the PDF"
    kill -SIGINT $$
fi

FILE=$1
PAGES=$(pdfinfo ${FILE} | grep 'Pages:' | sed 's/Pages:\s*//')

GRAYPAGES=""
COLORPAGES=""
DOUBLECOLORPAGES=""
DOUBLEGRAYPAGES=""
OLDGP=""
DOUBLEPAGE=0
DPGC=0
DPCC=0
SPGC=0
SPCC=0

echo "Pages: $PAGES"
N=1
while (test "$N" -le "$PAGES")
do
    COLORSPACE=$( identify -format "%[colorspace]" "$FILE[$((N-1))]" )
    echo "$N: $COLORSPACE"
    if [[ $DOUBLEPAGE -eq -1 ]]
    then
    DOUBLEGRAYPAGES="$OLDGP"
    DPGC=$((DPGC-1))
    DOUBLEPAGE=0
    fi
    if [[ $COLORSPACE == "Gray" ]]
    then
        GRAYPAGES="$GRAYPAGES,$N"
    SPGC=$((SPGC+1))
    if [[ $DOUBLEPAGE -eq 0 ]]
    then
        OLDGP="$DOUBLEGRAYPAGES"
        DOUBLEGRAYPAGES="$DOUBLEGRAYPAGES,$N"
        DPGC=$((DPGC+1))
    else 
        DOUBLEPAGE=0
    fi
    else
        COLORPAGES="$COLORPAGES,$N"
    SPCC=$((SPCC+1))
        # For double sided documents also list the page on the other side of the sheet:
        if [[ $((N%2)) -eq 1 ]]
        then
            DOUBLECOLORPAGES="$DOUBLECOLORPAGES,$N,$((N+1))"
        DOUBLEPAGE=$((N+1))
        DPCC=$((DPCC+2))
            #N=$((N+1))
        else
        if [[ $DOUBLEPAGE -eq 0 ]]
        then 
                DOUBLECOLORPAGES="$DOUBLECOLORPAGES,$((N-1)),$N"
        DPCC=$((DPCC+2))
        DOUBLEPAGE=-1
        elif [[ $DOUBLEPAGE -gt 0 ]]
        then
        DOUBLEPAGE=0            
        fi                      
        fi
    fi
    N=$((N+1))
done

echo " "
echo "Double-paged printing:"
echo "  Color($DPCC): ${DOUBLECOLORPAGES:1:${#DOUBLECOLORPAGES}-1}"
echo "  Gray($DPGC): ${DOUBLEGRAYPAGES:1:${#DOUBLEGRAYPAGES}-1}"
echo " "
echo "Single-paged printing:"
echo "  Color($SPCC): ${COLORPAGES:1:${#COLORPAGES}-1}"
echo "  Gray($SPGC): ${GRAYPAGES:1:${#GRAYPAGES}-1}"
#pdftk $FILE cat $COLORPAGES output color_${FILE}.pdf
