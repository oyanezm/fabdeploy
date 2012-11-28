from fabric.api import local,cd,settings,run,task
from fabric.api import env

def add_commit_pull(self):
    """
    deploy the application
    """
    commit()
    local_pull()

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
    clones the repo and set requires permissions
    """
    run("git clone %(git_addr)s %(project_name)s" % env)

