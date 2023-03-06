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
# type command >/dev/null 2>&1 && type getconf >/dev/null 2>&1 &&
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
if [ ! -d $file_dir ]; then
  mkdir $file_dir
fi
file_dir=${file_dir}/${year}
if [ ! -d $file_dir ]; then
  mkdir $file_dir
fi
file_dir=${file_dir}/${month}
if [ ! -d $file_dir ]; then
  mkdir $file_dir
fi
file_dir=${file_dir}/${uuid}
if [ ! -d $file_dir ]; then
  mkdir $file_dir
fi
file_dirS=${file_dir}/${syntax}
if [ ! -d $file_dirS ]; then
  mkdir $file_dirS
fi
file_dirC=${file_dir}/CSV
if [ ! -d $file_dirC ]; then
  mkdir $file_dirC
fi
# === copy uploaded file =============================================
mime-read file $Tmp-cgivars > $Tmp-uploadfile
filename=${file_dirS}/${name}
cp $Tmp-uploadfile ${filename}
# === Generate CSV ===================================================
basename=${name:0:-4}
csvfile=${file_dirC}/${basename}.csv
(
  java -classpath /ebs/www/sambuichi.jp/public_html/core-japan/server/core-japan-0.0.1.jar wuwei.japan_core.cius.Invoice2csv ${syntax} ${filename} ${csvfile}
) &
# wait $!
# STATUS="${?}"
# === Return result ==================================================
# cat <<HTML_CONTENT
# Content-Type:application/json

# {"invoice":"${filename}","csv":"${csvfile}","syntax":"${syntax}","uuid":"${uuid}"}
# HTML_CONTENT
result="uuid ${uuid}"
sleep 5
cat <<HTML_CONTENT
Content-Type:text/plane

${result}
HTML_CONTENT
rm -f $Tmp-*
exit 0
# invoice2csv.cgi
