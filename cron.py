from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import run,sudo,env,task 
from fabric.contrib import files
from fabdeploy.servers import get_server

@task
def configure():
    """
    configures cron jobs
    """
    context = _AttrDict(
        base_url = env.url,
        log_path = env.log_path + 'cron/execution.log',
    )

    generate_cron_file(context)
    set_crontab()
    delete_cron_file()

@task
def append():
    """
    adds cron job
    """
    # create tmp cron file
    generate_cron_file(context)

    # append existing crontab
    run('crontab -l >%s' % tmp_cron_path)
    set_crontab()
    delete_cron_file()


def set_crontab():
    run('crontab %s' % tmp_cron_path)

def generate_cron_file(contxt):
    """
    creates temporary cron file
    """

    # upload tmp file
    tmp_cron_path = env.cron_path + '.tmp'

    files.upload_template(
        filename = env.cron_path,
        destination = tmp_cron_path,
        use_sudo = env.use_sudo,
        context = contxt
    )

def remove_cron_file():
    run('rm %s' % tmp_cron_path)

