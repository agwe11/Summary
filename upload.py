import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import bulk
fn=sys.argv[1]
es = Elasticsearch("localhost:9200",http_auth=('elastic','hi4gz2llFltL5ZVpDhnN'))
try:
    #make the bulk call, and get a response
    response = helpers.bulk(es, bulk.bulk_json_data(fn+"/upload.json", "web_"+fn, "_doc"))
    print("\nResponse:",response)
except Exception as e:
    print('error',e)
