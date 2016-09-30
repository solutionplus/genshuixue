数据库操作

ssh -f worker@172.21.134.7 -L 3305:drdse7h0fv7cmp68.drds.aliyuncs.com:3306 -N

mysql -h127.0.0.1 -uzhanqun -pwdlPD40xjO5 -P3305
mysql> set names utf8;
mysql> source /Users/bjhl/Documents/tb_cidian.sql;


测试库
mysql -h172.21.139.2 -uatlas_rw -patlas_rw -P1234


导出部分表结构和数据（不能够有空格）
只导出结构
mysqldump --opt -d  -h172.21.139.2 -uatlas_rw -patlas_rw -P1234 zhanqun shici > shici.sql
导出结构与数据
mysqldump -h127.0.0.1 -uzhanqun -pwdlPD40xjO5  -P3305 zhanqun tb_cidian --where="id<200" > tb_cidian1.sql
mysqldump -h127.0.0.1 -uzhanqun -pwdlPD40xjO5  -P3305 zhanqun tb_cidian --where=' 1=1 limit 200' > tb_cidian_test.sql

权限问题
show global variables;

数据插入和显示编码
set names utf8;

按特定分隔符导出特定字段到特定文件
select taskid, result into outfile '/apps/home/rd/zengsheng/gwyjingyan_zhonggong.res' fields terminated by '$$$$$' from gwyjingyan_zhonggong ;

复杂的更新
UPDATE zhanqun.shiren SET evaluation = replace(evaluation,'<div class="open-tag-collapse" id="open-tag-collapse"/>','') where evaluation like '%<div class="open-tag-collapse" id="open-tag-collapse"/>%' 

生成结构相同的表
create table tb_new_query as select * from tb_query limit 0;

查询近30天的信息记录：
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy where date_sub(curdate(), INTERVAL 30 DAY) <= date(`date`);
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where to_days(now()) - to_days(`date`) <= 30;


查询昨天的信息记录：
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where to_days(now()) - to_days(`date`) <= 1;

查询今天的信息记录：
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where to_days(now()) - to_days(`date`) <= 0;
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where to_days(`date`) = to_days(now());

查询上个月的信息记录：
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where (date_format(now() , '%Y%m') - date_format(`date`, '%Y%m')) =1;
SELECT count(1) FROM zhanqun.keyword_monitor_fuzzy  where period_diff(date_format(now() , '%Y%m'),date_format(`date`, '%Y%m')) =1;

查询一个集群各个表当前数据量大小从高到低排名（以MB为单位）
select table_schema, table_name, Concat(Round(data_length / ( 1024 * 1024 ), 2), 'MB') As MB, table_rows from information_schema.tables order by MB desc

复杂的查询语句
select (case when (district like '%市' or district like '%区') then count(1)  when (district not like '%市' and  district not like '%区') then 0 end) as tal,city from `primary_school_info` where status=0 and (district like '%市' or district like '%区')  and city in ('北京','天津','上海','重庆','石家庄','郑州','武汉','长沙','南京','南昌','沈阳','长春','哈尔滨','西安','太原','济南','成都','西宁','合肥','海口','广州','贵阳','杭州','福州','台北','兰州','昆明','拉萨','银川','南宁','乌鲁木齐','呼和浩特','香港','澳门') group by city order by city
