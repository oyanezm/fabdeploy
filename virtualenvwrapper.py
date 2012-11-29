from fabdeploy.lib.utils import _AttrDict
from fabric.api import settings,run,env,local
from fabric.contrib import files

def prepare():
    """
    updates bash_profile  
    """
    conf = _AttrDict(
        bash_origin = ''.join([env.base,'/fabdeploy/config/.bash_profile']),
        bash_destiny = env.bash_profile,
        modules = ''.join([env.modules_path,'/bin/'])
        )
    files.upload_template(  filename = conf.bash_origin,
                            destination = conf.bash_destiny,
                            context = conf,
                            )

def venvsetup():
    """
    creates the virtualenvs root directory
    """
    conf = _AttrDict(
        venv_dir = ''.join([env.home,".virtualenvs"]),
        )
    with settings(warn_only=True):
        run('mkdir -p %(venv_dir)s' % conf)
        # just in case it already exists, let's ditch it
        run('rmvirtualenv %(project_name)s' % env)
    run('mkvirtualenv --no-site-packages %(project_name)s' % env)
