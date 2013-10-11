from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import run,sudo,env,task 
from fabdeploy.servers import get_server

@task
def configure():
    """
    configures apache based on Host
    """
    config = _AttrDict(
        wsgi = env.wsgi_path,
        home = env.home,
        root = env.path,
        admin = env.admin,
        server = ''.join(['www.',env.url]),
        venv_path = ''.join([env.home,'.virtualenvs/',env.project_name]),
        errorlog  = ''.join([env.log_path,'error.log']),
        accesslog = ''.join([env.log_path,'access.log']),
    )

    # get server and set configuration files
    server = get_server()
    server.configure(config)

def restart():
    """
    restart apache server
    """
    sudo('/etc/init.d/apache2 restart')
