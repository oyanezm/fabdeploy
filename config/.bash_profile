# fix https://bitbucket.org/dhellmann/virtualenvwrapper/issue/62/
if [ $USER = %(user)s ]; then
    export PYTHONPATH=%(modules)s
    export PATH=$HOME/.local/bin:$HOME/.local/:$PATH
    export WORKON_HOME=$HOME/.virtualenvs
    source %(modules)svirtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true
fi
