#! /usr/bin/env sh
#

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

# try time range 6:00 to 18:00 per 600 seconds(10mins)
# (18-6)*60/10=72
for count in {1..72}; do

  ./biwrapper_inner.sh

  if [ $? == 0 ]; then
    echo "success"
    break
  else
    echo "failed, try again"
    sleep 10
    continue
  fi
done
