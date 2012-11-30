from fabric.api import env,run,sudo,task
from fabdeploy import git,app
from fabdeploy.virtualenv import with_virtualenv
from pdb import set_trace as brake
from fabdeploy.servers import get_host

@task
def flush_repo():
    """
    removes the old repo in server and clones a new one.
    the configures the host.
    """
    host = get_host()
    run("rm -rf %(project_name)s" % env)
    git.clone()
    host.setup()

def prepare_deploy():
    """
    pull, commit, push and test in the app.
    """
    from fabdeploy.django import test as django_test
    django_test()
    git.add_commit_pull()
    git.push()

#TODO: find where to put static_path
def deploy_static():
    """
    empty static_root and collects the static files
    """ 
    from fabdeploy.django import collectstatic as django_collectstatic
#    run("rm -rf %(root_path)s%(project_name)s/static/*" % env) # call again git_add_commit_pull
    django_collectstatic()

@task(default=True)
def run(syncdb=False):
    """
    deploy the application to the server
    """
    from fabdeploy.django import migrate as django_migrate, syncdb as django_syncdb
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    prepare_deploy() # pull, test, push
    git.remote_pull()
    app.install_requirements()
    django_migrate(syncdb) # syncdb in case is first time
    deploy_static()

#TODO
def maintenance_up():
    """
    Install the Apache maintenance configuration.
    """
    run('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/%(project_name)s_maintenance %(apache_config_path)s' % env)
    reboot()

def maintenance_down():
    """
    Reinstall the normal site configuration.
    """
    install_apache_conf()
    reboot()
