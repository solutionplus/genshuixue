url='http://172.16.1.45:9200/corpora_index_v2_b/normal/'$1
echo $url
curl -XDELETE $url
