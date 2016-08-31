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

set names utf8;


UPDATE zhanqun.shiren SET evaluation = replace(evaluation,'<div class="open-tag-collapse" id="open-tag-collapse"/>','') where evaluation like '%<div class="open-tag-collapse" id="open-tag-collapse"/>%' 