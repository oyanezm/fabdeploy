from fabdeploy.lib.utils import _AttrDict, _is_host
from fabric.api import run,sudo,env,task 
from fabric.contrib import files
from fabdeploy.servers import get_server

@task
def configure():
    """
    configures cron jobs
    """
    config = _AttrDict(
        base_url = env.url,
        log_path = env.log_path + 'cron/execution.log',
    )

    # upload tmp file
    tmp_cron_path = env.cron_path + '.tmp'

    files.upload_template(
        filename = env.cron_path,
        destination = tmp_cron_path,
        use_sudo = env.use_sudo,
        context = config,
    )

    run('crontab %s' % tmp_cron_path)
    run('rm %s' % tmp_cron_path)

