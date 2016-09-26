数据库操作

ssh -f worker@172.21.134.7 -L 3305:drdse7h0fv7cmp68.drds.aliyuncs.com:3306 -N

mysql -h127.0.0.1 -uzhanqun -pwdlPD40xjO5 -P3305
mysql> set names utf8;
mysql> source /Users/bjhl/Documents/tb_cidian.sql;


测试库
mysql -h172.21.139.2 -uatlas_rw -patlas_rw -P1234


导出部分表结构和数据（不能够有空格）
mysqldump --opt -d  -h172.21.139.2 -uatlas_rw -patlas_rw -P1234 zhanqun shici > shici.sql
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
