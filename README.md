fab-deploy
==========

Deployment App based on Fabric

install
=======

add to fabfile.py:

from fabdeploy import fabulous
from fabdeploy import utils
loader, instances = fabulous.load_instances()
for inst in instances:
    loader(inst,__name__)
