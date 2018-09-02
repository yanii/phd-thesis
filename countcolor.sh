count=0; for file in thesis_*colorsplit.pdf; do num=`pdftk ${file} dump_data | grep NumberOfPages| awk '{print $2}'`;count=$((count + num)); echo $count; done; echo $count
