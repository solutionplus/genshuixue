Zhanqun search · last edited by 曾胜 28 days ago New Page Page History Edit Delete
目录

建立索引
索引从无到有的具体过程
查找接口
接口从无到有的具体过程
sitemap生成
建立索引

# mysql数据更新
10 * * * * source /apps/home/yuebin/.bash_profile && cd /apps3/yuebin/zhanqun-search && nohup /usr/local/bin/python -u index/hdfs_index_builder.py --manual --modify_time=100 > ./log/nohup_index_manual.log 2>&1
# 每日百站、经验增量数据
10 02 * * * source /apps/home/yuebin/.bash_profile && cd /apps3/yuebin/zhanqun-search && nohup /usr/local/bin/python -u index/hdfs_index_builder.py  --inc  --download  --delta=1> ./log/nohup_index_inc.log 2>&1
# 每日问答、题库增量数据
10 03 * * * source /apps/home/yuebin/.bash_profile && cd /apps3/yuebin/zhanqun-search && nohup /usr/local/bin/python -u index/hdfs_wenda_tiku_index_builder.py  --inc  --download  --delta=1> ./log/nohup_index_wenda_tiku_inc.log 2>&1
索引从无到有的具体过程

建立索引 
1、put索引corpora_index_v2_b，wenda_tiku_v1，original_query到zhanqun-es.baijiahulian.com:9200（即生成索引）
2、运行hdfs_index_builder.py，hdfs_wenda_tiku_index_builder.py，query_index.py，里面主要定义mapping和批量put数据到es中
3、在正式数据写入之前我们可以自己定义Mapping, 等数据写入时，会按照定义的Mapping进行映射。数据put到es中，es会自动生成索引。
查找接口

# zhanqun-serach.py
application = tornado.wsgi.WSGIApplication([
        (r"/v1/retrieve/?", pure_tornado_search.RetrieveHandlerV1),
        (r"/v1/retrieve_wt/?", pure_tornado_search.RetrieveWTHandlerV1),
        (r"/v1/original_query/?", pure_tornado_search.OriginalQueryHandlerV1),
        (r"/v1/detail_wt/?(.*)", pure_tornado_search.DetailWTHandlerV1),
        (r"/v1/detail/?(.*)", pure_tornado_search.DetailHandlerV1),
        (r"/v2/detail/?", pure_tornado_search.DetailHandlerV2),
        (r"/v1/multi_detail/?", pure_tornado_search.MultiDetailHandlerV1),
        (r"/v1/multi_index_cms/?", pure_tornado_search.IndexCMSRequestHandlerV1),
],**pure_tornado_search.settings)
接口从无到有的具体过程

创建接口 
比如/v1/retrieve/?接口
1、这个接口接收两个参数token（验证条件）以及params（要转成json）
2、根据params构建es的复合查询体b_body，查询es中的数据并经过一些处理返回json格式的数据
sitemap生成

# X 页面生成
45 09 * * 4 source /apps/home/yuebin/.bash_profile && cd /apps3/yuebin/zhanqun-search && nohup /usr/local/bin/python -u celery_landingpage.py > ./log/nohup_celery_job.log 2>&1
# sitemap生成
10 03 * * * source /apps/home/yuebin/.bash_profile && cd /apps3/yuebin/zhanqun-search && nohup /usr/local/bin/python -u sitemaps/gen_sitemaps.py > ./log/nohup_sitemaps.log 2>&1
X页面从无到有的具体过程

创建X页面 
1、通过接口/v1/retrieve/?得到一些数据
2、用python的一个中文分词插件SnowNLP对数据的content部分进行摘要提取
3、进一步使用random.sample，random.shuffle等函数使X页面生成更加成功
3、组合多个数据的内容构成一个X页面，提交给es