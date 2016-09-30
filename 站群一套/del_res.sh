project_name=$1
spider_machine=rd@172.16.10.1
ssh ${spider_machine} "cd /apps/home/rd/zengsheng && python del_res.py ${project_name}"
if [ $? -ne 0 ];then
    echo ${PROJECT_NAME} 'del resultdb fail'
    exit 1
fi
