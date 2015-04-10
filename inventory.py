#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To run this script you need requests and pyyaml
#
# $ virtuanenv somefolder
# $ cd somefolder
# $ source bin/activate
# $ easy_install pip
# $ pip install requests
# $ pip install pyyaml
# $ pip install ansible
#
# you now have a working ansible installation with the tools we need.
# save this script, the groups file and the configuration file to somefolder and you are ready to go.
#
# PS! remember to make the script executable
# $ chmod somefolder/inventory.py
#
# Test with:
#
# $ python inventory --list
# $ ansible ubuntu_all -m command -a "uptime" -u root -i somefolder/inventory.py
#
import requests
import sys
import json
import yaml
import ConfigParser


def configreader():
    """Read a configuration file.

    Attemt to read ansibleforeman.cfg from the folder we are located in, and from the users homefolder.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    config = ConfigParser.ConfigParser()
    readResult = config.read(['ansibleforeman.cfg'])

    # Configuration variables
    username = "blank_username"
    password = "blank_servername"
    foreman_url = "blank_foremanurl"
    groupfile = "groups.yml"

    # Try to read the configuration variables from the Main section
    try:
        username = config.get("Main", "username")
        password = config.get("Main", "password")
        foreman_url = config.get("Main", "foreman_url")
        groupfile = config.get("Others", "groupfile")
    except ConfigParser.NoSectionError:
        pass
    except ConfigParser.NoOptionError:
        pass

    readResult = {'username': username, 'password': password, 'foreman_url': foreman_url, 'groupfile': groupfile}

    return readResult

def get_hosts(hostfilter):
    payload = {'search':hostfilter + ' ', 'format': 'json', 'per_page': '1500', }
    r = s.get(configuration['foreman_url'], params=payload)
    return r.json()


# Read the configuration file
configuration = configreader()

# Read in the yaml groups file
f = open(configuration['groupfile'])
groups = yaml.safe_load(f)
f.close()

# Create a new http session with the following auth details and disabling ssl verification.
s = requests.Session()
s.auth = (configuration['username'], configuration['password'])
s.verify = False


#
# Ansible API requires that we implement the following two methods:
#
# hosts --list
# hosts --host HOSTNAME
#
# Both metod should return a json object
# ref: http://docs.ansible.com/developing_inventory.html
#
if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    # Create an empty dict to hold the results
    data = {}
    hostnamelist = []
    # Search for each individual group/filter
    for groupname, groupinfo in groups.iteritems():
        hostnamelist = []
        hosts = get_hosts(groupinfo['hostfilter'])

        for host in hosts:
            hostnamelist.append(host['host']['name'])

        data[groupname] = {'hosts': hostnamelist}

        if "vars" in groupinfo:
            data[groupname].update({'vars': groupinfo['vars']})

    print json.dumps(data, indent=2)

    sys.exit(0)

elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    # We want to lookup facts for a specific node
    hostname = sys.argv[2]
    payload = {'format': 'json'}
    r = s.get(configuration['foreman_url'] + "/" + hostname + "/" + "facts", params=payload)
    facts = r.json()
    print json.dumps(facts[hostname], indent=2)

    sys.exit(0)

else:
    print "usage: --list  ..OR.. --host <hostname>"
    sys.exit(1)


