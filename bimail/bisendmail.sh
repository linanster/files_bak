#! /usr/bin/env sh
#
workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

date=$(date +%F)
subject="BI Dashboard Database Daily Report ${date}"
from='nan2.li@ge.com'
tomail='zhe.hu@ge.com'
ccmail='nan2.li@ge.com,blake.xue@ge.com'
body='biquery.txt'

# mail -s "${subject}" nan2.li@ge.com < "${body}"
# mail -s "${subject}" -r ${from} nan2.li@ge.com < "${body}"
mail -s "${subject}" -r ${from} -c ${ccmail} ${tomail} < "${body}"
