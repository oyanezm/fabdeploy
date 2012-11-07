from fabdeploy.lib.helper import _AttrDict
from fabric.api import settings,run,env,local
from fabric.contrib import files

def with_virtualenv(command):
    """
    Executes a command in this project's virtual environment.
    """
    local("/bin/bash -l -c 'workon %s && %s'" % (env.project_name,command))

class _VirtualenvWrapperSetup(object):
    """
    class the holds methods for setting up the virtual enviroments and virtualenvwrapper.

    """
    def prepare(self):
        """
        class that crates the bash_profile reqiured for virtualenvwrapper
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

    def venvsetup(self):
        """
        Creates the virtualenvs root directory
        """
        conf = _AttrDict(
            venv_dir = ''.join([env.home,".virtualenvs"]),
            )
        with settings(warn_only=True):
            run('mkdir -p %(venv_dir)s' % conf)
            # just in case it already exists, let's ditch it
            run('rmvirtualenv %(project_name)s' % env)
        run('mkvirtualenv --no-site-packages %(project_name)s' % env)
