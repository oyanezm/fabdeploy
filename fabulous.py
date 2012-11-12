from pdb import set_trace as brake
from fabric.api import env,run,sudo
from fabdeploy import utils
from fabdeploy.apache import _ApacheSetup
from fabdeploy.database import _DatabaseSetup
from fabdeploy.git import _GitSuite,_GitHubHandler
from fabdeploy.virtualenv import _VirtualenvWrapperSetup,with_virtualenv
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
    return set_in_scope

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

    def prepare_deploy(self):
        """
        pull, commit, push and test in the app.
        """
        git = _GitSuite()
        app = _WebApp()
        app.test()
        git.add_commit_pull()
        git.push()

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
