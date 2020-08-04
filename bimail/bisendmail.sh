#! /usr/bin/env sh
#
workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

date=$(date +%F)
subject="BI Dashboard Database Daily Report ${date}"
tomail='zhe.hu@ge.com'
ccmail='nan2.li@ge.com,blake.xue@ge.com'
body='biquery.txt'

# mail -s "${subject}" nan2.li@ge.com < "${body}"
mail -s "${subject}" -c ${ccmail} ${tomail} < "${body}"
