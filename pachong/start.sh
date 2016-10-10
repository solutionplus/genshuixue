
nohup pyspider -c demo.json scheduler&
nohup pyspider -c demo.json phantomjs&
nohup pyspider -c demo.json --phantomjs-proxy 127.0.0.1:25555 fetcher --xmlrpc&
nohup pyspider -c demo.json processor&
nohup pyspider -c demo.json result_worker&
nohup pyspider -c demo.json webui&
# --scheduler-rpc http://127.0.0.1:23333 --fetcher-rpc http://127.0.0.1:24444&

tail -f nohup.out

