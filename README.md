###Requirements
To run this script you need requests and pyyaml

###Installation
    $ virtuanenv somefolder
    $ cd somefolder
    $ source bin/activate
    $ easy_install pip
    $ pip install requests
    $ pip install pyyaml
    $ pip install ansible

You now have a working ansible installation with the tools we need.
Save this script, the groups file and the configuration file to somefolder and you are ready to go.

PS! remember to make the script executable
$ chmod somefolder/inventory.py

###Test it
Test with:
    $ python inventory --list
    $ ansible ubuntu_all -m command -a "uptime" -u root -i somefolder/inventory.py
