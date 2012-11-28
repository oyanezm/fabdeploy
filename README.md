fab-deploy
==========

Deployment for Django based on Fabric > 1.5. Early Development not properly tested yet, be aware.

install
=======
This module comes with submodules for specific applications.
To install them you must (1) call the configurator to set the enviroment variables
and (2)import the modules you require. To do so:
```python
#1 load the modules you need
from fabdeploy import app, apache,github,django, deploy, database, 
#2 configure
from fabdeploy import configure
configure(__name__)
```
