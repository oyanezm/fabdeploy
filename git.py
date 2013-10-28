from fabric.api import local,cd,settings,run,task
from fabric.api import env

def add_commit_pull():
    """
    deploy the application
    """
    commit()
    local_pull()

def commit():
    """
    add files and ask for staging
    and commits.
    """
    with settings(warn_only = True):
        local("git add -p && git commit")

def push():
    """
    push to the repository
    """
    local("git push origin master")

def remote_pull():
    """
    pull locally from the repository
    """
    run("cd %(root_path)s; git pull origin master" % env)

@task
def pull():
    """
    pull the repository from ther server
    """
    local("git pull origin master")

def revert(commit_id):
    """
    reverts to a previous commit
    """
    local("cd %(git_addr)s; git reset --hard $(commit_id)s" % env)

def clone():
    """
    clones the repo and set requires permissions
    """
    run("git clone %(git_addr)s %(project_name)s" % env)

