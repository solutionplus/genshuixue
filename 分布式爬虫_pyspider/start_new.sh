#start only one scheduer
#nohup pyspider -c demo.json scheduler&
#start js-proxy ,in some pace phantomjs is also only one
nohup pyspider -c config_new.json phantomjs&
# start fetcher ,processor , result_worker as many as you  need
count=1
while [ ${count} -le 2 ]
do
    nohup pyspider -c config_new.json --phantomjs-proxy="localhost:25555"  fetcher&
    nohup pyspider -c config_new.json processor&
    nohup pyspider -c config_new.json result_worker&
    echo "${count} start"
    count=`expr ${count} + 1`
done
#start webui ,set '--scheduer-rpc' if scheduler is not runing on the same host with your webui instance
nohup pyspider -c config_new.json webui --scheduler-rpc http://172.26.251.162:23333&