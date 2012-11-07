from fabdeploy.lib.helper import _AttrDict, _is_host
from fabric.api import settings,run,sudo,env 
from fabdeploy.servers import _Alwaysdata, get_host
from pdb import set_trace as brake

class _ApacheSetup(object):
    """
    holds methods for installing site on apache
    """


    def install_site(self):
        """
        adds the virtualhost to apache
        """
        host = get_host()
        config = _AttrDict(
            wsgi = env.wsgi_path,
            admin = env.admin,
            server = env.server,
                root = env.path,
                home = env.home,
            template_path = env.conf_template,
            venv_path = ''.join([env.home,'.virtualenvs/',env.project_name]),
            errorlog = ''.join([env.path,'log/apache_error.log']),
            accesslog = ''.join([env.path,'log/apache_access.log']),
            )

        host.configure(config)
        with settings(warn_only = True):
            # remove logs
            run("rm -rf %(errorlog)s %(accesslog)s" % config)
        if env.use_sudo:
            sudo("chown root:root %s" % env.vhost_path)
            self.restart_apache()
        host.setup()

    def restart_apache(self):
        """
        restart apache server
        """
        sudo('/etc/init.d/apache2 restart')
