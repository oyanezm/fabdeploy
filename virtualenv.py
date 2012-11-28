from fabric.api import run,env,local

def with_virtualenv(command):
    """
    Executes a command in this project's virtual environment.
    """
    local("/bin/bash -l -c 'workon %s && %s'" % (env.project_name,command))
#    return result

def with_virtualenv_remote(command):
    """
    Executes a command in this project's virtual environment.
    """
    run("/bin/bash -l -c 'workon %s && %s'" % (env.project_name,command))

