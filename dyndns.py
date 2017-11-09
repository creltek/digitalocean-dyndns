from os import environ
from time import sleep
from requests import get, put
import json


def get_public_ip():
    return get("https://api.ipify.org").text

def get_record_id(domain, host, key):
    headers = {
        "Content-Type":"application/json"
        , "Authorization": "Bearer {}".format(key)
    }
    
    url = "https://api.digitalocean.com/v2/domains/{}/records".format(domain)

    resp = json.loads(get(url, headers=headers).text)

    for record in resp["domain_records"]:
        if record["name"] == host:
            return record["id"]
    
    raise Exception("Record Not Found")

def update_record(domain, record_id, ip, key):
    headers = {
        "Content-Type":"application/json"
        , "Authorization": "Bearer {}".format(key)
    }
    
    data = {"data":ip}
    
    url = "https://api.digitalocean.com/v2/domains/{}/records/{}".format(domain, record_id)
    
    return json.loads(put(url, data=json.dumps(data), headers=headers).text)["domain_record"]
    
if __name__ == "__main__":
    interval = int(environ.get("INTERVAL", 300))
    
    for var in ["DOMAIN", "HOST", "KEY"]:
        if var not in environ:
            raise Exception("{} Not Defined".format(var))
    
    host = environ["HOST"]
    domain = environ["DOMAIN"]
    key = environ["KEY"]

    last_ip = ""
    record_id = get_record_id(domain, host, key)
    
    while True:
        ip = get_public_ip()
        print("Public IP: {}".format(ip))
        
        if ip != last_ip:
            record = update_record(domain, record_id, ip, key)
            print("Updated Record: {} {}".format(record["id"], ip))
        
        last_ip = ip
        
        sleep(interval)
 