#! /usr/bin/env sh
#

echo **Query Time: $(date -d "+8 hours" "+%F %T")** > biquery.txt
echo "**This is automatic mail, please do not reply!**" >> biquery.txt

echo>> biquery.txt
echo ==1.Summary Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select * from GE.summary order by statistics_time desc limit 5;' >> biquery.txt
echo>> biquery.txt
echo ==2. Active Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select * from GE.active order by statistics_time desc limit 5;' >> biquery.txt
echo>> biquery.txt
echo ==3. Device_produced Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select created_time,sum(produced_count) from GE.device_produced group by created_time order by created_time desc limit 5;' >> biquery.txt
echo>> biquery.txt
echo ==4. Device Table== >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select count(appliance_id) as 'Total' from GE.device;' >> biquery.txt
mysql -hestar.xlink.cloud -uroot -pGEMysql20200 -e 'select device_type, count(appliance_id) as 'count' from GE.device group by device_type order by count desc;' >> biquery.txt





