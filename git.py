from fabric.api import local,cd,settings,run
from fabric.api import env
class _GitSuite(object):
    """
    hold methods to use git
    """

    def add_commit_pull(self):
        """
        deploy the application
        """
        self.commit()
        self.local_pull()

    def commit(self):
        """
        add files and ask for staging
        and commits.
        """
        with settings(warn_only = True):
            local("git add -p && git commit")

    def push(self):
        """
        push to the repository
        """
        local("git push origin master")

    def remote_pull(self):
        """
        pull locally from the repository
        """
        run("cd %(path)s; git pull origin master" % env)

    def local_pull(self):
        """
        pull the repository from ther server
        """
        local("git pull origin master")

    def revert(self,commit_id):
        """
        reverts to a previous commit
        """
        local("cd %(git_addr)s; git reset --hard $(commit_id)s" % env)

    def clone(self):
        """
        clones the repo
        """
        run("rm -rf %(project_name)s" % env)
        run("git clone %(git_addr)s %(project_name)s" % env)

class _GitHubHandler(object):
    """
    handler to deal with github secure connection
    """
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

    def ssh_setup(self):
        """
        backup the old keys and set the new ones
        """
        self.backup_ssh()
        self.generate_key()
