from fabric.api import run, env
from fabric.contrib import files
from pdb import set_trace as brake

class _BaseHost(object):
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

class _Alwaysdata(_BaseHost):
    """
    always data config setup
    """
    name = "alwaysdata"

    def setup(self):
        """
        adds the configuration file
        """
        filename = 'django.fcgi'
        fcgi_origin = '/'.join(env.conf_template.split('/')[:-1]+[filename])
        fcgi_destiny = '/'.join(env.wsgi_path.split('/')[:-1]+[filename])
#        put(fcgi_origin,fcgi_destiny)
        run("chmod +x %s" % fcgi_destiny)

class _Localhost(_BaseHost):
    """
    localhost configuration
    """
    name = "localhost"

    def configure(self,config):
        """
        updates an apache config file
        """
        files.upload_template(  filename = config.template_path, 
                                destination = env.vhost_path,
                                use_sudo = env.use_sudo,
                                context = config,
                                )
def get_host():
    """
    returns the host class
    """
    for hostname in env.hosts:
        if "alwaysdata" in hostname:
            return _Alwaysdata()
        elif "localhost" in hostname:
            return _Localhost()

