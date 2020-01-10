# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys
from collections import defaultdict
import json
import subprocess
import bulk
from headercheck import check_safeh
from retire import get_jsfile
import ip2asn

es = Elasticsearch("localhost:9200")
dict = defaultdict(dict)
ip_to_ports = defaultdict(list)
apps = defaultdict(list)
ssllab={}

#create dict with massdns results/ip2asn
with open("./hyundai.com/online.txt") as origin_file:
    for line in origin_file:
        domain = line.split()[0][:-1]
        if "A " in line:
            ip = line.split()[2]
            str_to_ip= ip2asn.convert_str_to_ip(ip)
            as_number, as_description, country_code = ip2asn.search_asn(str_to_ip)

            dict.update({domain:{'ip': ip,'asn':{'number': as_number,'desc':as_description,'country_code':country_code}}})

        elif "CNAME " in line:
            cname = line.split()[2]
            dict.update({domain:{'cname' : cname}})

with open("ssl.txt") as fp:
    for line in fp:
        parts = line.strip().split(":")
        ssllab.update({parts[0].replace('"',""):parts[1].replace('"',"")})
'''
if i['status']== 'ERROR':
    dict[i['host']].update({'ssl': i['statusMessage']})
elif i['endpoints'][0]['statusMessage'] == 'Ready':
    dict[i['host']].update({'ssl': {' notafter': datetime.fromtimestamp(float(i['certs'][0]['notAfter'])/1000.)}})
timestamp = data[6]['certs'][0]['notAfter']
ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
timestamp = float(data[6]['certs'][0]['notAfter'])/1000.
t = datetime.fromtimestamp(float(data[6]['certs'][0]['notAfter'])/1000.)

wapp domain
list(data[0]['urls'].keys())[0].split('//')[1][:-1]
if len(i['applications']) >> 1:
    dict[list(i['urls'].keys())[0].split('//')[1][:-1]].update({'applications':[i['applications']]})

file = open('ssl.txt','r')
json.load(file)


'''
#find open ports from masscan result
with open('masscang.txt') as fp:
    for line in fp:
        if line.startswith('Host:'):
            parts = line.strip().split()
            ip = parts[1]
            port = parts[-1]
            # split it by '/' and grab the first element
            port = port.split('/')[0]
            # add ip and ports to our defaultdict
            # if the ip isn't in the defaultdict, it will be created with
            # an empty set, that we can add the port to.
            # if we run into the same port twice, 
            # the second entry will be ignored.
            ip_to_ports[ip].append(port)
#append ports to dict
for k,v in dict.items():
    for ip in ip_to_ports:
        if ip == v["ip"]:
         dict[k].update({"ports" : ip_to_ports[ip]})

#append ssllabscan grade to ip
for k,v in dict.items():
    for ip in ssllab:
        if ip == v["ip"]:
            dict[k].update({"ssllabgrade" : ssllab[ip]})
#append url
for k,v in dict.items():
    if dict[k].get("ports"):
        ports = dict[k].get("ports")
        print(dict[k])
        if '443' in ports : 
            dict[k].update({"urls": "https://"+k})
            #dict[k].update({"missingheaders": check_safeh(dict[k]["urls"])})
            dict[k].update({"retirejs" : get_jsfile("https://"+k)})
        elif '80' in ports and '443' not in ports:
            dict[k].update({"urls": "http://"+k})
            #dict[k].update({"missingheaders": check_safeh(dict[k]["urls"])})
            dict[k].update({"retirejs" : get_jsfile("http://"+k)})
        dict[k].update(check_safeh(k))
        print(dict[k])    
#append applications
with open('wapp.txt') as fp:
    for line in fp:
        if "http" in line:
            parts = line.strip().split(': ')
            url = parts[0][:-2][1:]
            application = parts[-1]
            apps[url].append(application.replace('"',''))
            #print(apps)
for k,v in dict.items():
    if dict[k].get("urls"):
        for a in apps:
            if a == v["urls"]:
                dict[k].update({"applications" : apps[a]})

#prepare elasticsearch bulk upload
for k,v in dict.items():
    print(dict[k].get("missingheaders"))
    doc = { "domain" : k, "ip": v["ip"], "ports": dict[k].get("ports"), "urls": dict[k].get("urls"),"applications": dict[k].get("applications"),"missingheaders":dict[k].get("missingheaders"),"headergrade":dict[k].get("headergrade"), "retirejs": dict[k].get("retirejs"),"ssllabgrade": dict[k].get("ssllabgrade")}
    with open('upload.json', 'a') as out:
#        out.write('{"index":{"_id": "'+doc["domain"]+'"}}\n')
        out.write('{}\n'.format(json.dumps(doc)))
#    print(doc)
#print(dict)
#def get_data_from_text_file(self):
#    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]
#    docs = get_data_from_text_file('upload.json')
#    dict_doc = json.loads(doc)
#    print(dict_doc)


try:
    #make the bulk call, and get a response
    response = helpers.bulk(es, bulk.bulk_json_data("upload.json", "test", "doc"))
    print ("\nbulk_json_data() RESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)
