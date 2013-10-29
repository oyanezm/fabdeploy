from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import run,sudo,env,task 
from fabric.contrib import files
from fabdeploy.servers import get_server


# upload tmp file
tmp_cron_path = env.cron_path + '.tmp'

@task
def configure():
    """
    configures cron jobs
    """
    env.log_path += 'cron/execution.log',

    generate_cron_file()
    set_crontab()
    delete_cron_file()

@task
def append():
    """
    adds cron job
    """
    # create tmp cron file
    generate_cron_file()

    # append existing crontab
    run('crontab -l >%s' % tmp_cron_path)
    set_crontab()
    delete_cron_file()


def set_crontab():
    run('crontab %s' % tmp_cron_path)

def generate_cron_file():
    """
    creates temporary cron file
    """

    files.upload_template(
        filename = env.cron_path,
        destination = tmp_cron_path,
        use_sudo = env.use_sudo,
        context = env
    )

def remove_cron_file():
    run('rm %s' % tmp_cron_path)

