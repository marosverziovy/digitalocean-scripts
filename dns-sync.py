#!/usr/bin/python

import requests

API_URL = 'https://api.digitalocean.com'
TOKEN = 'xxx'
ZONE = 'domain.com'
SUBDOMAIN = 's'

class dnsSync:

    # returns list() [{server, ip}]
    def get_server_details(self):
        r = requests.get(API_URL + '/v2/droplets', auth=(TOKEN, ''))
        mapping = []
        for droplet in r.json()['droplets']:
            for interface  in droplet['networks']['v4']:
                if interface['type'] == 'public':
                    mapping.append({'name': droplet['name'], 'public_ip': interface['ip_address']})
        return(mapping)

    # checks whether the record is present
    # and makes sure the record is set to correct ip
    def check_if_exists(self, server, ip):
        r = requests.get(API_URL + '/v2/domains/{}/records'.format(ZONE), auth=(TOKEN, ''))
        for record in r.json()['domain_records']:
            if record['type'] == 'A':
                if record['name'] == str('{}.{}'.format(server, SUBDOMAIN)):
                    return(True)
                else:
                    pass

    # updates actual record
    def add_record(self, server, ip):
        zone = {
              "type": "A",
              "name": '{}.{}'.format(server, SUBDOMAIN),
              "data": ip
            }
        r = requests.post(API_URL + '/v2/domains/{}/records'.format(ZONE), auth=(TOKEN, ''), json=zone)
        return(r.json())

    def sync(self):
        for server in self.get_server_details():
            if self.check_if_exists(server['name'], server['public_ip']) != True:
                self.add_record(server['name'], server['public_ip'])

d = dnsSync()
d.sync()