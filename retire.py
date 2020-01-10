import requests
from bs4 import BeautifulSoup
import re
import retirejs
from requests.compat import urljoin
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions
from collections import defaultdict
import sys
import json
fn = sys.argv[1]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'}
def get_jsfile(url):
    dict = {}
    d=""
    script = []
    s = Session()
    s.mount('https://',HTTPAdapter(max_retries=Retry(total=3)))
    try:
        r = s.get(url,verify=False,allow_redirects=True,timeout=5,headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        script = soup.find_all("script", src=re.compile(".js"))
    except Exception as e:
        print(e)
        pass

    print(len(script)) 
    if len(script) > 1:
        temp = []
        vuln = []
        for i in script:
            if i['src'].startswith('http'):
                jsfile = i['src']
            else:    
                jsfile = urljoin(r.url,i['src'])
            print(jsfile)
            for e in range(2):
                
                    try:
                      temp = retirejs.scan_endpoint(jsfile)
                      vuln.append(temp)
                      #vuln.append(temp[0]['component'] +":"+  temp[0]['version'])
                      #print(vuln)
                      #dict['test'].append(vuln)
                      #print(dict)
                      break
                    except:
                        continue
        vuln = list(filter(None, vuln))
        if len(vuln) > 1 :
            dict[url.split('//')[1]] = vuln
            f = open(fn+'/retire.txt','a')
            print(json.dumps(dict), file=f)
        #return vuln
    else:
        return None
with open(fn+'/urls.txt') as fp:
    for line in fp:
        print(line)
        get_jsfile(line.strip())
#print(dict)
#get_jsfile('https://org-www.kia.com')
