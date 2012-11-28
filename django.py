from fabdeploy.virtualenv import _VirtualenvWrapperSetup, with_virtualenv,\
                                 with_virtualenv_remote
from fabric.api import cd,sudo,env,task

@task(name='admin')
def django_admin(command):
    """
    runs a django-admin command
    """
    config_path = ("%(base)s/%(project_name)s/config/dev/" % env)
    return("cd %s;python manage.py %s" % (config_path,command))

@task(name='test')
def django_test():
    """
    unit testing on app.
    """
    if env.avoid_test:
        return True
    from fabric.contrib.console import confirm
    from fabric.api import abort
    result = with_virtualenv(django_admin("test"))

@task
def collect_static(self):
    """
    calls collect static files
    """
    result = with_virtualenv_remote(django_admin("collectstatic"))

@task
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