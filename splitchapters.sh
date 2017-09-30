#!/bin/bash
infile=$1 # input pdf
outputprefix=thesis/

[ -e "$infile" -a -n "$outputprefix" ] || exit 1 # Invalid args

pagenumbers=( $(pdftk "$infile" dump_data | \
		grep -A1 '^BookmarkLevel: 1' | grep '^BookmarkPageNumber: ' | cut -f2 -d' ' | uniq)
              end )

chapternames=( $(pdftk "$infile" dump_data | \
		grep -B1 '^BookmarkLevel: 1' | grep '^BookmarkTitle: ' | cut -f2- -d' ' | tr ' ' '-'| uniq)
              end )
for ((i=0; i < ${#pagenumbers[@]} - 1; ++i)); do
  a=${pagenumbers[i]} # start page number
  b=${pagenumbers[i+1]} # end page number
  [ "$b" = "end" ] || b=$[b-1]
  pdftk "$infile" cat $a-$b output "${outputprefix}"${chapternames[i]}.pdf
done
