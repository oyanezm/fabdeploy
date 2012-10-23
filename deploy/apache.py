from deploy.lib.helper import _AttrDict, _is_host
from fabric.api import settings,run,sudo 
from fabric.contrib import files
from deploy.servers import _Alwaysdata

class _ApacheSetup(object):
    """
    holds methods for installing site on apache
    """

    def install_site(self):
        """
        adds the virtualhost to apache
        """
        conf = _AttrDict(
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

        files.upload_template(  filename = conf.template_path, 
                                destination = env.vhost_path,
                                use_sudo = env.use_sudo,
                                context = conf,
                                )
        with settings(warn_only = True):
            # remove logs
            run("rm -rf %(errorlog)s %(accesslog)s" % conf)
        if env.use_sudo:
            sudo("chown root:root %s" % env.vhost_path)
            self.restart_apache()
        # only for alwaysdata
        if _is_host(env.hosts,'alwaysdata'):
            adata = _Alwaysdata()
            adata.alwaysdata_setup()

    def restart_apache(self):
        """
        restart apache server
        """
        sudo('/etc/init.d/apache2 restart')
