file_name=$1
echo "$file_name"
head -n1 "$file_name" > temp_header
sed '1d' "$file_name" > temp
gshuf temp > temp2
mv temp2 temp
line_count=`cat temp|wc -l`
line_per_file=`echo $line_count|awk '{x=int($1/2); if(x*2==$1){print x;}else{print x+1;}}'`
echo $line_per_file
gsplit -l $line_per_file -d temp "$file_name."
for i in 0 1
do
    fn="$file_name.0$i"
    echo $fn
    cat temp_header "$fn" > "$fn.h"
    mv "$fn.h" "$fn" 
done
rm temp
rm temp_header
