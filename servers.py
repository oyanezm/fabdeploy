from fabric.api import run, env, put
from fabric.contrib import files
from pdb import set_trace as brake

class _BaseServer(object):
    """
    base class that holds safe methods
    """
    def setup(self):
        """
        dummy setup
        """
        pass

    def configure(self,dummy):
        """
        dummy config
        """
        pass

    def set_permissions(self):
        """
        dummy permissions
        """
        pass


class _Alwaysdata(_BaseServer):
    """
    always data config setup
    """
    name = "alwaysdata"

    def setup(self):
        """
        adds the configuration file
        """
        filename = '.htaccess'
        origin = '/'.join(env.vhost_template.split('/')[:-1]+[filename])
        destiny ='/'.join(env.wsgi_path.split('/')[:-1]+[filename])
        put(origin,destiny)
        self.set_permissions()

    def set_permission(self):
        """
        gives exec permissions to fcgi files
        """
        fcgi_destiny = '/'.join(env.wsgi_path.split('/')[:-1]+['django.fcgi'])
        run("chmod +x %s" % fcgi_destiny)

class _Localhost(_BaseServer):
    """
    localhost configuration
    """
    name = "localhost"

    def configure(self,config):
        from fabric.api import settings,sudo,env
        """
        updates apache virtualhosts
        """
        filename = env.url; # use url as filename e.g foo.bar.com
        sites_enabled_path = ''.join([env.apache_path,'sites-enabled/',filename]);
        sites_available_path = ''.join([env.apache_path,'sites-available/',filename]);

        # wipe data logs, virtualhost config
        with settings(warn_only = True):
            run("rm -rf %(errorlog)s %(accesslog)s" % config)
            run("rm -rf %s" % sites_available_path)
            run("rm -rf %s" % sites_enabled_path)

        # upload file
        files.upload_template(
            filename = env.vhost_template,
            destination = sites_available_path,
            use_sudo = env.use_sudo,
            context = config,
        )

        # set permitions and restart apache
        if env.use_sudo:
            sudo("chown root:root %s" % sites_available_path)
            sudo("ln -s %s %s" % (sites_available_path, sites_enabled_path) )
            sudo('/etc/init.d/apache2 restart')

def get_server():
    """
    returns the host class
    """
    for hostname in env.hosts:
        if "alwaysdata" in hostname:    return _Alwaysdata()
        else:                           return _Localhost()

