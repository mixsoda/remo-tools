#%%
# Nature remo sensor id finder

#import
import requests
import json

#read token
f = open('../token.txt')
token = f.readline().replace('\n','').replace('\r','')

#get appliances list
url = "https://api.nature.global/1/appliances"
headers = {"content-type": "application/json", "Authorization": "Bearer "+token}
r = requests.get(url, headers=headers)
print("JSON :", r.status_code)

#perse json
data = r.json()

#%%
#display id list
print("<< Nature remo >>")
print("remo NAME     = ", data[0]["device"]["name"])
print("remo ID       = ", data[0]["device"]["id"])
print("remo MAC addr = ", data[0]["device"]["mac_address"])

for app in data :
    print("")
    print("NAME : ", app["nickname"], "(TYPE:", app["type"], ")")
    print("ID=", app["id"])



#%%
