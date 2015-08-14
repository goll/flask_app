# flask_app

## Overview
Exercise Flask application with MongoDB and JSON.

## Requirements
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Ansible](https://docs.ansible.com/ansible/intro_installation.html)

## Installation
To locally provision a Vagrant machine (CentOS 7.1) with the running application run these commands:

    $ git clone https://github.com/goll/flask_app.git
    $ cd flask_app/
    $ vagrant up

## Usage
The application has two endpoints: `/add` and `/show`.  
When the machine is provisioned the application will be available on `http://localhost:8080`.  
The application is served by nginx connected to a gunicorn instance.  
The gunicorn instance can be controlled with the `flask.service` systemd unit file.  
For quick usage I recommend using [Postman](https://www.getpostman.com) for the GET and POST requests.  
All responses are JSON formatted.

### /add endpoint
The `http://localhost:8080/add` endpoint accepts JSON data as a POST request in this format:

    [
        {
            "uid": "1",
            "name": "John Doe",
            "date": "2015-05-12T14:36:00.451765",
            "md5checksum": "e8c83e232b64ce94fdd0e4539ad0d44f"
        },
        {
            "uid": "2",
            "name": "Jane Doe",
            "date": "2015-05-13T14:36:00.451765",
            "md5checksum": "13065eda9a6ab62be1e63276cc7c46b0"
        }
    ]

If the md5checksum of the date, uid and name fields (e.g. `{"date": "2015-05-12T14:36:00.451765", "uid": "1", "name": "John Doe"}`) matches the value of the JSON md5checksum field, the entry will be saved to MongoDB, otherwise it is discarded.

### /show endpoint
The `http://localhost:8080/show` endpoint accepts a GET request with 2 parameters: `uid` and `date`.  
When queried, the application will return the number of occurrences of a given uid for that day.  

e.g. response for query `http://localhost:8080/show?uid=1&date=2015-05-12`

    {
        "date": "2015-05-12",
        "occurrences": 1,
        "success": "true",
        "uid": 1
    }

## Tests
The application uses unittest to verify everything is working. To run the tests inside the provisioned machine run these commands from the project directory (`flask_app/`):

    $ vagrant ssh
    $ sudo su -
    # source /usr/share/nginx/venv/bin/activate
    # python2 /usr/share/nginx/dr_test.py

## Debug mode
To run the application in debug mode inside the provisioned machine, stop the services and run it manually:

    # systemctl stop nginx
    # systemctl stop flask
    # source /usr/share/nginx/venv/bin/activate
    # python2 /usr/share/nginx/dr.py

## Local install
To run the application locally in debug mode without Vagrant you need `python-virtualenv` and `mongodb-server` installed and running.  
Then run these commands from the project directory (`flask_app/`):

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r provisioning/files/requirements.txt
    $ python2 provisioning/files/dr.py

The application listens on *:8080.