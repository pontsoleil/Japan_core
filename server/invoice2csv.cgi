#!/bin/bash
# === Initialize shell environment ===================================
set -euvx # identify cause error on some pdf file. so drop -e
# -e  Exit immediately if a command exits with a non-zero status.
# -u  Treat unset variables as an error when substituting.
# -v  Print shell input lines as they are read.
# -x  Print commands and their arguments as they are executed.
export LC_ALL=C
export PATH=".:./bin:$(command -p getconf PATH)${PATH+:}${PATH-}"
export UNIX_STD=2003  # to make HP-UX conform to POSIX
Tmp=/tmp/${0##*/}.$$
# === Log ============================================================
exec 2>log/${0##*/}.$$.log
type command >/dev/null 2>&1 && type getconf >/dev/null 2>&1 &&
# === Upload directory ===============================================
datetime=$(date '+%Y-%m-%d_%H:%M:%S')
year=$(date '+%Y')
month=$(date '+%2m')
uuid=$(uuidgen)
# === Uploaded contents ==============================================
dd bs=${CONTENT_LENGTH:-0} count=1 > $Tmp-cgivars
syntax=$(mime-read syntax $Tmp-cgivars)
name=$(mime-read -v $Tmp-cgivars                                         | # tee log/${0##*/}.$$.step1.log |
grep -Ei '^[0-9]+[[:blank:]]*Content-Disposition:[[:blank:]]*form-data;' | # tee log/${0##*/}.$$.step2.log |
grep '[[:blank:]]name="file"'                                            | # tee log/${0##*/}.$$.step3.log |
head -n 1                                                                | # tee log/${0##*/}.$$.step4.log |
sed 's/.*[[:blank:]]filename="\([^"]*\)".*/\1/'                          | # tee log/${0##*/}.$$.step5.log |
sed 's/[[:space:]]/_/g')                                                 # escape space
# === Check file directory ===========================================
file_dir='data'
if [ ! -d $file_dir ]; then
  mkdir $file_dir
fi
# file_dir=${file_dir}/${year}
# if [ ! -d $file_dir ]; then
#   mkdir $file_dir
# fi
# file_dir=${file_dir}/${month}
# if [ ! -d $file_dir ]; then
#   mkdir $file_dir
# fi
# file_dir=${file_dir}/${uuid}
# if [ ! -d $file_dir ]; then
#   mkdir $file_dir
# fi
file_dirXML=${file_dir}/${syntax}
if [ ! -d $file_dirXML ]; then
  mkdir $file_dirXML
fi
file_dirCSV=${file_dir}/CSV
if [ ! -d $file_dirCSV ]; then
  mkdir $file_dirCSV
fi
# === copy uploaded file =============================================
mime-read file $Tmp-cgivars > $Tmp-uploadfile
xmlfile=${file_dirXML}/${name}
cp $Tmp-uploadfile ${xmlfile}
# === Syntax binding CSV =============================================
basename=${name:0:-4}
workfile=${file_dirCSV}/${basename}_work.csv
(
  java -classpath core-japan-0.0.1.jar wuwei.japan_core.cius.Invoice2csv ${syntax} ${xmlfile} ${workfile}
) &
wait $!
STATUS0="${?}"
# === Transpose CSV ==================================================
csvfile=${file_dirCSV}/${basename}.csv
transposedfile=${file_dirCSV}/${basename}_transposed.csv
(
  python3 transpose.py ${workfile} -c ${csvfile} -t ${transposedfile}
) &
wait $!
STATUS="${?}"
# === Generate CSV ===================================================
csv_contents=$(cat $csvfile|awk '{print}' ORS='\\n')
escaped=$(echo $csv_contents|sed 's/\"/\\"/g'|sed 's/\r//g'|tr -d '\n')
transposed_contents=$(cat $transposedfile|awk '{print}' ORS='\\n')
escaped_transposed=$(echo $transposed_contents|sed 's/\"/\\"/g'|sed 's/\r//g'|tr -d '\n')
# === Return result ==================================================
cat <<HTML_CONTENT
Content-Type:application/json

{"return":"${STATUS}","uuid":"${uuid}","syntax":"${syntax}","xmlfile":"${xmlfile}","csvfile":"${csvfile}","csv_contents":"${escaped}","transposedfile":"${transposedfile}","transposed_contents":"${escaped_transposed}"}
HTML_CONTENT
# rm -f $Tmp-*
exit 0
# invoice2csv.cgi
