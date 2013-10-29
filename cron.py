from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import run,sudo,env,task 
from fabric.contrib import files
from fabdeploy.servers import get_server
from pdb import set_trace as brake


@task
def configure():
    """
    configures cron jobs
    """
    env.log_path += '/cron/execution.log',

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
    run('crontab -l >%s' % env.cron_path_tmp)
    set_crontab()
    delete_cron_file()


def set_crontab():
    run('crontab %s' % env.cron_path_tmp)

def generate_cron_file():
    """
    creates temporary cron file
    """

    files.upload_template(
        filename    = env.cron_path,
        destination = env.cron_path_tmp,
        use_sudo    = env.use_sudo,
        context     = env
    )

def remove_cron_file():
    run('rm %s' % env.cron_path_tmp)

