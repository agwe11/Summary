import json 
ID = 2 
     ...: output = set() 
     ...: output_list = [] 
     ...: for i in temp_list: 
     ...:      
     ...:     output.add(i['desc']) 
     ...: for k in output: 
     ...:     output_list.append({'id':ID,'name':k,'parent':1}) 
     ...:     ID += 1 
     ...: output = set() 
     ...: for i in temp_list: 
     ...:     output.add(i['cidr']) 
     ...: for k in output: 
     ...:     output_list.append({'id':ID,'name':k,'parent':lookup_id('cidr',k,'desc')}) 
     ...:     ID += 1 
     ...:          
     ...: output = set() 
     ...: for i in temp_list: 
     ...:     output.add(i['ip']) 
     ...: for k in output: 
     ...:     output_list.append({'id':ID,'name':k,'parent':lookup_id('ip',k,'cidr')}) 
     ...:     ID += 1 
     ...: output = set() 
     ...: for i in temp_list: 
     ...:     output.add(i['domain']) 
     ...: for k in output: 
     ...:     output_list.append({'id':ID,'name':k,'parent':lookup_id('domain',k,'ip')}) 
     ...:     ID += 1 


''' 
ID = 2 
output_list = [] 
temp = {} 
#asn_desc 
temp_list = [] 
def lookup_id(field,name,rtn_field):  
    for i in temp_list:
        if i[field] == name:
            value = i[rtn_field]
    for k in output_list:  
         if k['name'] == value:  
             return k['id']  
 
 
with open('upload.json','r') as fp:  
     output = set()  
     for line in fp:  
         temp = json.loads(line)  
         if 'asn' in temp.keys():  
            temp_list.append({'desc':temp['asn']['desc'],'cidr':temp['asn']['cidr'],'ip': temp['ip'],'domain':temp['domain']}) 



def lookup_id(name): 
     for k in output_list: 
         if k['name'] == name: 
             return k['id'] 


with open('upload.json','r') as fp: 
     output = set() 
     for line in fp: 
         temp = json.loads(line) 
         if 'asn' in temp.keys(): 
            output.add({'id': ID,'name':temp['asn']['desc'],'parent':2})
            
            ID += 1
#asn-cidr
with open('upload.json','r') as fp: 
     output = set() 
     for line in fp: 
         temp = json.loads(line) 
         if 'asn' in temp.keys(): 
             output_list.append({'id': ID,'name':temp['asn']['cidr'],'parent':lookup_id(temp['asn']['desc'])})
             ID += 1

'''
