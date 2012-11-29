# it has underscore in name because __init__.py we must call the standard django framework.
from fabdeploy.virtualenv import with_virtualenv, with_virtualenv_remote
from fabric.api import cd,sudo,env,task

@task
def admin(command):
    """
    runs a django-admin command
    """
    config_path = ("%(base)s/%(project_name)s/config/dev/" % env)
    return("cd %s;python manage.py %s" % (config_path,command))

def test():
    """
    unit testing on app.
    """
    if env.avoid_test:
        return True
    from fabric.contrib.console import confirm
    from fabric.api import abort
    result = with_virtualenv(django_admin("test"))

def collectstatic(self):
    """
    calls collect static files
    """
    result = with_virtualenv_remote(django_admin("collectstatic"))

def syncdb():
    """
    runs django-admin.py syncdb
    """
    with_virtualenv_remote(django_admin("syncdb"))

def django__migrate(self,app_name=''):
    with_virtualenv_remote(django_admin("migrate %s" % app_name))

def initial_migration(self,app_name):
    with_virtualenv_remote(django_admin("schemamigration %s --initial" % app_name))

def auto_migration(self,app_name):
    with_virtualenv_remote(django_admin("schemamigration %s --auto" % app_name))
