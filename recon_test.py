from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys
from collections import defaultdict
import json
import subprocess
import bulk
from datetime import datetime
import ip2asn
import os,glob
import base64
<<<<<<< HEAD
import takeover
=======

>>>>>>> 8760796f056798aa5867d3b49082e5612d622ba0
es = Elasticsearch("localhost:9200")
dict = defaultdict(dict)
ip_to_ports = defaultdict(list)
apps = defaultdict(list)
fn = sys.argv[1]
#create dict with massdns results/ip2asn
with open(fn+"/online.txt") as origin_file:
    for line in origin_file:
        domain = line.split()[0][:-1]
        if ". A " in line:
            ip = line.split()[2]
            str_to_ip= ip2asn.convert_str_to_ip(ip)
            as_number, as_description, country_code,cidrs = ip2asn.search_asn(str_to_ip)

            dict.update({domain:{'ip': ip,'asn':{'number': as_number,'desc':as_description,'country_code':country_code,'cidr':cidrs}}})

        elif ". CNAME " in line:
            cname = line.split()[2]
<<<<<<< HEAD
            cnameurl = 'http://'+cname
            status,content = takeover.request(cnameurl,None,5)
            service,error = takeover.checker(status,content)
            if service and error:
                dict.update({domain:{'cname': cname,'subdomaintakeover':{'service':service,'message':'potential TAKEOVER vulnerability found!'}}})
            else:
                dict.update({domain:{'cname' : cname}})
=======
            dict.update({domain:{'cname' : cname}})
>>>>>>> 8760796f056798aa5867d3b49082e5612d622ba0
#import pdb;pdb.set_trace()
with open(fn+"/ssl.txt") as fp:
    ssllab = json.load(fp)
    for i in ssllab:
        if i['status']== 'ERROR':
            dict[i['host']].update({'ssl': {'status': i['statusMessage']}})
        elif i['endpoints'][0]['statusMessage'] == 'Ready':
            t = datetime.fromtimestamp(float(i['certs'][0]['notAfter'])/1000.)
            t = t.strftime('%Y/%m/%d')
            dict[i['host']].update({'ssl': {' notafter': t,'grade':i['endpoints'][0]['grade']}})


'''
if i['status']== 'ERROR':
    dict[i['host']].update({'ssl': i['statusMessage']})
elif i['endpoints'][0]['statusMessage'] == 'Ready':
    dict[i['host']].update({'ssl': {' notafter': datetime.fromtimestamp(float(i['certs'][0]['notAfter'])/1000.)}})
timestamp = data[6]['certs'][0]['notAfter']
ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
timestamp = float(data[6]['certs'][0]['notAfter'])/1000.
t = datetime.fromtimestamp(float(data[6]['certs'][0]['notAfter'])/1000.)

headers
for k,v in headers.items():
    dict[k].update({headers:v})

wapp domain
data = []
with open('wapp.txt') as fp:
    for line in fp:
        data.append(json.loads(line))
list(data[0]['urls'].keys())[0].split('//')[1][:-1]
if len(i['applications']) >> 1:
    dict[list(i['urls'].keys())[0].split('//')[1][:-1]].update({'applications':i['applications']})

file = open('ssl.txt','r')
json.load(file)


'''
#wapp
data = []
with open(fn+'/wapp.txt') as fp:
    for line in fp:
        data.append(json.loads(line))
for i in data:
    if len(i['applications']) >> 1:
        dict[list(i['urls'].keys())[0].split('//')[1][:-1]].update({'applications':i['applications']})

#headers
with open(fn+'/headercheck.txt') as fp:
     for line in fp:
         temp = json.loads(line)
         for k,v in temp.items():
             dict[k].update({"headers":v})
#retirejs
with open(fn+'/retire.txt') as fp:
     for line in fp:
         temp = json.loads(line)
         for k,v in temp.items():
             dict[k].update({"retirejs":v}) 
#find open ports from masscan result
with open(fn+'/massg.txt') as fp:
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
    if 'ip' in v.keys():
        for ip in ip_to_ports:
            if ip == v["ip"]:
             dict[k].update({"ports" : ip_to_ports[ip]})
#append urls
with open(fn+'/urls.txt') as fp:
    for line in fp:
        dict[line.split('//')[1].rstrip()].update({"urls": line.rstrip()})

#base64 png
folder_path = '/home/agwe11/python/webscreenshot/'+fn 

for filename in glob.glob(os.path.join(folder_path,'*_thumb.png')):
    
    with open(filename,'rb') as fp:

        str = base64.b64encode(fp.read()).decode('utf-8')
        dict[filename.split('_')[1]].update({'screenshot':'data:image/png;base64,'+str})

#append ssllabscan grade to ip
#for k,v in dict.items():
#    for ip in ssllab:
#        if ip == v["ip"]:
#            dict[k].update({"ssllabgrade" : ssllab[ip]})
##append url
#for k,v in dict.items():
#    if dict[k].get("ports"):
#        ports = dict[k].get("ports")
#        print(dict[k])
#        if '443' in ports : 
#            dict[k].update({"urls": "https://"+k})
#            #dict[k].update({"missingheaders": check_safeh(dict[k]["urls"])})
#            dict[k].update({"retirejs" : get_jsfile("https://"+k)})
#        elif '80' in ports and '443' not in ports:
#            dict[k].update({"urls": "http://"+k})
#            #dict[k].update({"missingheaders": check_safeh(dict[k]["urls"])})
#            dict[k].update({"retirejs" : get_jsfile("http://"+k)})
#        dict[k].update(check_safeh(k))
#        print(dict[k])    
##append applications
#with open(fn+'wapp.txt') as fp:
#    for line in fp:
#        if "http" in line:
#            parts = line.strip().split(': ')
#            url = parts[0][:-2][1:]
#            application = parts[-1]
#            apps[url].append(application.replace('"',''))
#            #print(apps)
#for k,v in dict.items():
#    if dict[k].get("urls"):
#        for a in apps:
#            if a == v["urls"]:
#                dict[k].update({"applications" : apps[a]})

#prepare elasticsearch bulk upload
for k,v in dict.items():
#    print(dict[k].get("missingheaders"))
#    doc = { "domain" : k, "ip": v["ip"], "ports": dict[k].get("ports"), "urls": dict[k].get("urls"),"applications": dict[k].get("applications"),"missingheaders":dict[k].get("missingheaders"),"headergrade":dict[k].get("headergrade"), "retirejs": dict[k].get("retirejs"),"ssllabgrade": dict[k].get("ssllabgrade")}
    doc = {"domain":k}
    doc.update(v)
    with open(fn+'/upload.json', 'a') as out:
#        out.write('{"index":{"_id": "'+doc["domain"]+'"}}\n')
        print(json.dumps(doc),file=out)
#    print(doc)
#print(dict)
#def get_data_from_text_file(self):
#    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]
#    docs = get_data_from_text_file('upload.json')
#    dict_doc = json.loads(doc)
#    print(dict_doc)


#try:
#    #make the bulk call, and get a response
#    response = helpers.bulk(es, bulk.bulk_json_data("upload.json", "test", "doc"))
#    print ("\nbulk_json_data() RESPONSE:", response)
#except Exception as e:
#    print("\nERROR:", e)
