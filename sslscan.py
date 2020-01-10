dict = {}
with open('/home/agwe11/amass/kia.com/ssl.txt') as fp:
    for line in fp:
        parts = line.strip().split(":")
        dict.update({parts[0].replace('"',""):parts[1].replace('"',"")})
print(dict["195.2.220.213"])
