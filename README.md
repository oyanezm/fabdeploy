fab-deploy
==========

Deployment App based on Fabric

install
=======
add to fabfile.py:
```python
from fabdeploy import fabulous
#bound to the current module
loader, instances = fabulous.load_instances()
for inst in instances:
    loader(inst,__name__)
```
