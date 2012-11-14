from fabdeploy.virtualenv import _VirtualenvWrapperSetup, with_virtualenv,\
                                 with_virtualenv_remote
from fabdeploy.lib.helper import _AttrDict
from fabric.api import cd,sudo,settings,run,env,local

class _WebAppSetup(object):
    """
    holds methods for setting up and deploying a web application.
    """

    def install_requirements(self):
        """
        install virtualenv requirements from requirements.txt
        """
        with cd(env.path):
            with_virtualenv('pip install -r requirements.txt')

    def bootstrap_setup(self):
        """
        Setup a fresh virtualenv as well as a few useful directories, then run
        a full deployment
        """
        conf = _AttrDict(
            bash_profile = env.bash_profile,
            modules = env.modules_path,
            )
        venv_sup = _VirtualenvWrapperSetup()
        if env.use_sudo:
            sudo('apt-get install python-setuptools apache2 libapache2-mod-wsgi')
            sudo('easy_install pip')
            flag = ''
        else:
            flag = '--install-option="--user"'
            with settings(warn_only=True):
                run("rm %(bash_profile)s" % conf)
                run("rm -rf %(modules)s" % conf)
#            run("mkdir %(modules)s" % conf)

        venv_sup.prepare()
        run('pip install %s virtualenv' % flag)
        run('pip install %s virtualenvwrapper' % flag)
        venv_sup.venvsetup()

        self.install_requirements()

class _WebApp(object):
    """
    Handler to use some web application functions.
    """

    def test(self):
        """
        unit testing on app.
        """
        if env.avoid_test:
            return True
        from fabric.contrib.console import confirm
        from fabric.api import abort
        config_path = ("%(base)s/%(project_name)s/config/dev/" % env)
        result = with_virtualenv("cd %s;python manage.py test" % config_path)
#        if result.failed and not confirm("Test Failed. Contnue Anyway?"):
#            abort("aborting at user request.")

    def collect_static(self):
        """
        calls collect static files
        """
        config_path = ("%(path)s%(project_name)s/config/%(step)s/" % env)
        result = with_virtualenv_remote("cd %s;python manage.py collectstatic" % config_path)
