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
@task
def test():
    """
    unit testing on app.
    """
    if env.avoid_test:
        return True
    from fabric.contrib.console import confirm
    from fabric.api import abort
    result = with_virtualenv(admin("test"))
@task
def collectstatic():
    """
    calls collect static files
    """
    result = with_virtualenv_remote(admin("collectstatic"))

def syncdb():
    """
    runs django-admin.py syncdb
    """
    with_virtualenv_remote(admin("syncdb"))
@task
def migrate(use_syncdb = False, app_name=''):
    """
    run migrations on "app_name".
    use_syncdb in case its first time to migrate
    """
    if use_syncdb:
        syncdb()
    with_virtualenv_remote(admin("migrate %s" % app_name))

def initial_migration(app_name):
    with_virtualenv_remote(admin("schemamigration %s --initial" % app_name))

def auto_migration(app_name):
    with_virtualenv_remote(admin("schemamigration %s --auto" % app_name))
