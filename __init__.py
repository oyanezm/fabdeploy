import sys, os
from pdb import set_trace as brake
from fabric.api import env,task
from fabdeploy.lib import utils, import_non_local

# Base Path
env.base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(env.base)

# JSON Config Path
conf_path = ''.join([env.base,'/fabdeploy/config/fab_conf.json'])

import json
config = json.loads(open(conf_path).read())

def set_db_data(env):
    """
    set database variables to env
    """
    # if using django load from settings
    if env.settings_django_package:

        import_non_local('django','django_std')
        from django_std.conf import settings as django_settings
        from fabric.contrib import django

        django.settings_module(env.settings_django_package)

        env.db_user = django_settings.DB_USER
        env.db_pass = django_settings.DB_PASSWORD
        env.db_name = django_settings.DB_NAME
        env.site_url = django_settings.SITE_URL

    # otherwise use json settings
    else:
        json_settings = json.loads(open(env.settings_json).read())

        env.db_user = json_settings['DB_USER']
        env.db_pass = json_settings['DB_PASSWORD']
        env.db_name = json_settings['DB_NAME']
        env.site_url = json_settings['SITE_URL']

    # SET BACKUP VARS
    import datetime
    env.today_backup_folder = env.backup_path + '/' + str(datetime.date.today())
    env.today_backup_gzip = env.today_backup_folder + '.tgz';

    # SET CRON VARS
    env.cron_path_tmp = env.cron_path + '/crontab.tmp'


def env_setter(step):
    """
    closure that sets the enviroment.
    """
    def set_in_scope():
        """
        sets the host env
        """
        env.step = step
        utils.copy_keys(env,config[env.step])
        utils.copy_keys(env,config['globals'])
        set_db_data(env)
    return set_in_scope

def configure(module_name):
    """
    bound the dev,stage and prod tasks
    to the current module.
    """
    from types import MethodType
    steps = ['dev','test','live']

    # get the module as an object
    module_obj = sys.modules[module_name]

    # bound the tasks
    for step in steps:
        funcs = task(env_setter(step))
        funcs.name = step
        method = MethodType(funcs,module_obj,module_obj.__class__)
        setattr(module_obj,step,funcs)

    # if no env, use default
    if not set(steps).intersection(set(sys.argv)):
        env_setter(steps[0])();

