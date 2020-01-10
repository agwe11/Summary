import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import bulk
fn=sys.argv[1]
es = Elasticsearch("localhost:9200",http_auth=('elastic','letmein1#L'))
try:
    #make the bulk call, and get a response
    response = helpers.bulk(es, bulk.tree_bulk_json_data(fn+"/tree.json", "tree_"+fn, "_doc"))
    print("\nResponse:",response)
except Exception as e:
    print('error',e)
