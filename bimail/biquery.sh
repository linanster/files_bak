#! /usr/bin/env sh
#

echo **Query Time: $(date "+%F %T")** > biquery.txt
echo "**This is automatic mail, please do not reply!**" >> biquery.txt

echo>> biquery.txt
echo ==1.Summary Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select * from GE.summary order by statistics_time desc limit 5;' >> biquery.txt
echo>> biquery.txt
echo ==2. Active Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select * from GE.active order by statistics_time desc limit 5;' >> biquery.txt

