from fabric.api import env,run,sudo
from fabdeploy import utils
from fabdeploy.apache import _ApacheSetup
from fabdeploy.database import _DatabaseSetup
from fabdeploy.git import _GitSuite,_GitHubHandler
from fabdeploy.virtualenv import _VirtualenvWrapperSetup,with_virtualenv
from fabdeploy.servers import get_host
from fabdeploy.webapp import _WebAppSetup, _WebApp

import sys,os
env.base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(env.base)
conf_path = ''.join([env.base,'/fabdeploy/config/fab_conf.json'])

import json
config = json.loads(open(conf_path).read())

def env_setter(step):
    """
    closure that sets the enviroment.
    """
    def set_in_scope(args):
        env.step = step
        utils.copy_keys(env,config[env.step])
        utils.copy_keys(env,config['globals'])
        set_db_data(env.settings_module)
    return set_in_scope

def set_db_data(settings_module):
    """
    set database variables to env
    """
    from django.conf import settings as django_settings
    from fabric.contrib import django
    django.settings_module(settings_module)
    env.db_user = django_settings.DB_USER
    env.db_pass = django_settings.DB_PASSWORD
    env.db_table = django_settings.DB_NAME

class _Roles(object):
    """
    set the roles for dev, stagging and production
    """
    def __init__(self):
        from types import MethodType
        steps = ['dev','stage','prod']
        for step in steps:
            funcs = env_setter(step)
            method = MethodType(funcs,self,self.__class__)
            setattr(self,step,method)

class _Deploy(object):
    """
    hold methods for deploying of the applicantion.
    """

    def flush_repo(self):
        """
        removes the old repo in server and clones a new one.
        the configures the host.
        """
        host = get_host()
        git = _GitSuite()
        run("rm -rf %(project_name)s" % env)
        git.clone()
        host.setup()

    def prepare_deploy(self):
        """
        pull, commit, push and test in the app.
        """
        git = _GitSuite()
        app = _WebApp()
        app.test()
        git.add_commit_pull()
        git.push()
    #TODO: find where to put static_path
    def deploy_static(self):
        """
        empty static_root and collects the static files
        """
        run("rm -rf %(path)s%(project_name)s/static/*" % env)
        app = _WebApp()
        app.collect_static()

    def deploy(self):
        """
        deploy the application to the server
        """
        import time
        git = _GitSuite()
        wapp = _WebAppSetup()
        env.release = time.strftime('%Y%m%d%H%M%S')
        self.prepare_deploy()
        git.remote_pull()
        self.deploy_static()
#        wapp.install_requirements()

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

def load_instances():
    instances = [_Roles(),
                _DatabaseSetup(),
                _VirtualenvWrapperSetup(),
                _ApacheSetup(),
                _WebAppSetup(),
                _Deploy(),
                _WebApp(),
                _GitSuite(),
                _GitHubHandler(),]
    return utils.class_methods_to_functions, instances
