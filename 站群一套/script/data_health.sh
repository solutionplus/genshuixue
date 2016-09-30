project_name=$1
node_id=$2
python spider_db_tools.py download $project_name
echo 'download file finish!'
python spider_db_tools.py health $project_name $node_id
echo 'data health check finish!'
