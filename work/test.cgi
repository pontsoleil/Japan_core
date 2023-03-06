#!/bin/sh
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
# === Upload directory ===============================================
datetime=$(date '+%Y-%m-%d_%H:%M:%S')
year=$(date '+%Y')
month=$(date '+%2m')
uuid=$(uuidgen)
result="uuid 8a09f613-1797-4764-a359-8290cec8d0db"
# === Return result ==================================================
cat <<HTML_CONTENT
Content-Type:text/plane

${result}
HTML_CONTENT
# cat <<HTML_CONTENT
# Content-Type: application/json

# {"year":"${year}","month":"${month}","uuid":"${uuid}"}
# HTML_CONTENT
rm -f $Tmp-*
exit 0
# test.cgi