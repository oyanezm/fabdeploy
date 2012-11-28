fab-deploy
==========

Deployment for Django based on Fabric > 1.5. Early Development not properly tested yet, be aware.

install
=======
add to fabfile.py:
```python
from fabdeploy import fabulous
#bound to the current module
_loader, instances = fabulous.load_instances()
for inst in instances:
    _loader(inst,__name__)
```
