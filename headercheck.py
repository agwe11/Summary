import requests
from bs4 import BeautifulSoup
import sys
import json
fn= sys.argv[1]

requests.packages.urllib3.disable_warnings() 
#client_headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0)\
# Gecko/20100101 Firefox/53.0',
#    'Accept': 'text/html,application/xhtml+xml,\
# application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'en-US;q=0.8,en;q=0.3',
#    'Upgrade-Insecure-Requests': '1'
# }
#
## Security headers that should be enabled
#
#sec_headers = {
#    'X-XSS-Protection': 'warning',
#    'X-Frame-Options': 'warning',
#    'X-Content-Type-Options': 'warning',
#    'Strict-Transport-Security': 'error',
#    'Public-Key-Pins': 'none',
#    'Content-Security-Policy': 'warning',
#    'X-Permitted-Cross-Domain-Policies': 'warning',
#    'Referrer-Policy': 'warning'
#}
#
#def check_safeh(url):
#    missingheaders = []
#    try:
#        r = requests.get(url,verify=False,timeout=3,headers=client_headers)
#        for safeh in sec_headers:
#            if safeh not in r.headers:
#                missingheaders.append(safeh)
#        return missingheaders
#    except requests.exceptions.ConnectionError:
#        return 'connection error'
#    except requests.exceptions.ConnectTimeout:
#        return 'connection timeout'
#    except requests.exceptions.SSLError:
#        return 'ssl error'
#    except:
#        return 'error'
def check_safeh(domain):
    headers = []
    dict = {}
    try:
        r = requests.get('https://securityheaders.com/?q='+domain+'&followRedirects=on',verify=False,timeout=5)
        if "Sorry about that" in r.text:
            raise ValueError
    except ValueError:
        pass
    except:
        pass
    try:
        r = requests.get('https://securityheaders.com/?q=http://'+domain+'&followRedirects=on',verify=False,timeout=5)
        if "Sorry about that" in r.text:
            raise ValueError
    except ValueError:
        pass
    except:
        pass
    try:

        r = requests.get('https://securityheaders.com/?q=https://'+domain+'&followRedirects=on',verify=False,timeout    =5)
        if "Sorry about that" in r.text:
            return {"missingheaders":"error","headergrade":"error"}
    except:
        return {"missingheaders":"error","headergrade":"error"}
    soup = BeautifulSoup(r.content,'html.parser')
    soupheader = soup.findAll('th', {"class": "tableLabel table_red"})
    grade = soup.find('div', {"class": "score"}).findNext('span').text

    for i in soupheader:
        headers.append(i.text)
    #print(headers)
    dict[domain] = {"missingheaders":headers,"headergrade":grade}
    #dict[domain]["headergrade"] = grade
    f = open(fn+'/headercheck.txt','a')
    print(json.dumps(dict), file=f)
    print(json.dumps(dict))

with open(fn+'/domains.txt') as fp:
    for line in fp:
        check_safeh(line.strip())
#check_safeh("vpntest.hyundai.com")


