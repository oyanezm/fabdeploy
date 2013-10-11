# Fabdeploy

Deployment for Django based on Fabric > 1.5. Early Development not
properly tested yet, be aware.

## Installation
This module comes with submodules for specific applications.
To install them you must (1) import the modules you require and
(2) call the configurator to set the enviroment variables.
To do so add to your fabfile:

```python
#1 load the modules you need
from fabdeploy import app, apache, github, django, deploy, database 
#2 configure
from fabdeploy import configure
configure(__name__)
```

## Configure
In *'fabdeploy/config/fab_conf.example'* you find the configuration
file format. This must be renamed to *'fab_conf.json'*.

There you will find:

* globals
* dev
* test
* live
