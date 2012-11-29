from fabdeploy.virtualenv import with_virtualenv,with_virtualenv_remote
from fabdeploy import virtualenvwrapper as venvwrapper
from fabdeploy.lib.utils import _AttrDict
from fabric.api import cd,sudo,settings,run,env,local,task

@task
def install_requirements():
    """
    install virtualenv requirements from requirements.txt
    """
    with cd(env.path):
        with_virtualenv('pip install -r requirements.txt')

@task(name='setup')
def bootstrap_setup():
    """
    setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    conf = _AttrDict(
        bash_profile = env.bash_profile,
        modules = env.modules_path,
        )
    if env.use_sudo:
        sudo('apt-get install python-setuptools apache2 libapache2-mod-wsgi')
        sudo('easy_install pip')
        flag = ''
    else:
        flag = '--install-option="--user"'
        with settings(warn_only=True):
            run("rm %(bash_profile)s" % conf)
            run("rm -rf %(modules)s" % conf)
        run("mkdir %(modules)s" % conf)

    venvwrapper.prepare()
    run('pip install %s virtualenv' % flag)
    run('pip install %s virtualenvwrapper' % flag)
    venvwrapper.venvsetup()

    install_requirements()
