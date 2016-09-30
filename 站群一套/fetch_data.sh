#!/bin/bash
project_name=$1
cur_data_path=$2
#spider_machine=worker@182.92.163.136
spider_machine=rd@172.16.10.1
#spider_path=/apps/home/worker/yangxiaoyun/dist-spider
spider_path=/apps/home/rd/hexing/dist-spider
spider_script_path=${spider_path}/script
spider_result_path=${spider_path}/result/${project_name}.res
ssh $spider_machine "cd $spider_script_path && sh download.sh $project_name"
if [ $? -ne 0 ];then
    echo 'download ${project_name} data fail'
    exit 1
fi
scp ${spider_machine}:$spider_result_path ${cur_data_path}
if [ $? -ne 0 ];then
    echo 'scp ${project_name} data fail'
    exit 2
fi
