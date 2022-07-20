#!/usr/bin/python

import requests
from requests.structures import CaseInsensitiveDict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--server', type=str, required=True)
parser.add_argument('--id', type=str, required=True)
parser.add_argument('--auth_key', type=str, required=True)
parser.add_argument("-c", "--command", type=str, required=True)
args = parser.parse_args()
#print(f"shelly_one.py --server {args.server} --id {args.id} --auth_key '***' -c {args.command}")

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

def main():
    
    if args.command == 'relay_state' or args.command == 'cloud_state':
        get_state(args.command, args.id, args.auth_key, args.server)
    elif args.command == 'on' or args.command == 'off':
        control(args.command, args.id, args.auth_key, args.server)
    else:
        print("[ERROR] unknown command")

def get_state(state, id, key, server):
    url = f"{server}/device/status"
    data = f"id={id}&auth_key={key}"
    resp = requests.post(url, headers=headers, data=data)
    if state == 'relay_state':
        print(resp.json()['data']['device_status']['relays'][0]['ison'])
    elif state == 'cloud_state':
        print(resp.json()['data']['online'])
    else:
        print("[ERROR] unknown command")

def control(command, id, key, server):
    url = f"{server}/device/relay/control"
    data = f"channel=0&turn={command}&id={id}&auth_key={key}"
    requests.post(url, headers=headers, data=data)

if __name__ == "__main__":
    main()