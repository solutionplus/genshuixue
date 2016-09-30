source ~/.bashrc
cnt=15
nohup  pyspider -c config.json scheduler&
# phantomjs
nohup  pyspider -c config.json phantomjs&
#nohup pyspider -c config.json fetcher&
#debug和run时两套代码
i=0
while(($i<$cnt))
do
	nohup  pyspider -c config.json --phantomjs-proxy="localhost:25555" fetcher&
	nohup  pyspider -c config.json processor&
	nohup  pyspider -c config.json result_worker&
	i=$(($i+1))
	echo $i' start'
done
nohup  pyspider -c config.json webui&
