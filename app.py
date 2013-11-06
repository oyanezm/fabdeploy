from fabric.api import cd,sudo,settings,run,env,local,task
from pdb import set_trace as brake

def backup_to_gzip():
    """
    compress backup folder to gzip and wipe folder
    """
    from fabdeploy import apache

    # Gzip folder and remove
    with settings(warn_only = True):
        run('tar -cvzpf ' + env.today_backup_gzip + ' -C ' + env.today_backup_folder + ' . >/dev/null 2>&1')
        run('rm -rf ' + env.today_backup_folder)
        run('rm -f '+ env.log_path + '/apache/*')
        run("echo '*\n!.gitignore' > "+ env.log_path + "/apache/.gitignore")
        apache.restart()

@task
def backup():
    """
    store sql and logs in backup folder
    """
    from fabdeploy import database as db

    # dump sql
    db.dump()

    # Store public files to backup folder
    print("\nStoring Public files")
    with settings(warn_only = True):
        for public_path in env.public_path:
            run('cp -r ' + public_path + ' ' + env.today_backup_folder)

    # Store log files
    print("\nStoring Log Files")
    with settings(warn_only = True):
        run('cp ' + env.log_path + '/apache/* '+ env.today_backup_folder)

    # backup folder to gzip
    print("\nCompressing Backup")
    backup_to_gzip()

def install_requirements():
    """
    install virtualenv requirements from requirements.txt
    """
    from fabdeploy.virtualenv import with_virtualenv_remote
    with cd(env.root_path):
        with_virtualenv_remote('pip install -r requirements.txt')

def setup():
    """
    setup a fresh virtualenv as well as a few useful directories
    then run a full deployment
    """
    from fabdeploy import virtualenvwrapper as venvwrapper
    from fabdeploy.lib.utils import _AttrDict
    conf = _AttrDict(
        bash_profile = env.bash_profile_path,
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
