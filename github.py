from fabric.api import cd,run,settings,task
def backup_ssh(self):
    """
    ssh key backup.
    """
    with cd('~/.ssh') and settings(warn_only = True):
        run('mkdir key_backup')
        run('cp id_rsa* key_backup')
        run('rm id_rsa*')

def generate_key(self):
    """
    generates the ssh key
    """
    # assumed admin
    env.email = env.admin
    with cd('~/.ssh'):
        run('ssh-keygen -t rsa -C "%(email)s"' % env)
@task
def setup(self):
    """
    backup the old keys and set the new ones
    """
    backup_ssh()
    generate_key()
