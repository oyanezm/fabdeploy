from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import settings,run,sudo,env,task 
from fabdeploy.servers import get_host

@task
def configure(self):
    """
    configures apache based on Host
    """
    config = _AttrDict(
        wsgi = env.wsgi_path,
        admin = env.admin,
        server = env.server,
            root = env.root_path,
            home = env.home,
        vhost_path = env.vhost_template,
        venv_path = ''.join([env.home,'.virtualenvs/',env.project_name]),
        errorlog  = ''.join([env.log_path,'error.log']),
        accesslog = ''.join([env.log_path,'access.log']),
    )

    # get host and set configuration files
    host = get_host()
    host.configure(config)

    # remove old logs
    with settings(warn_only = True):
        run("rm -rf %(errorlog)s %(accesslog)s" % config)

    if env.use_sudo:
        sudo("chown root:root %s" % env.vhost_path)
        restart()

    host.setup() # ony for alwatsdata TODO: reorganize

def restart(self):
    """
    restart apache server
    """
    sudo('/etc/init.d/apache2 restart')
