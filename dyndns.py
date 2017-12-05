from os import environ
from time import sleep
from requests import get, put
import json
import getopt
import sys

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
    options, args = getopt.getopt(sys.argv[1:], "h:d:k:", ["host=", "domain=", "key="])

    host = ""
    domain = ""
    key = ""

    for option, a in options:
        if option in("-h", "--host"):
            host = str(a)

        elif option in("-d", "--domain"):
            domain = str(a)

        elif option in("-k", "--key"):
            key = str(a)
            
    interval = int(environ.get("INTERVAL", 300))

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
