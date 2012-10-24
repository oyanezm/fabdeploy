from fabric.api import run

class _Alwaysdata(object):
    """
    always data config setup
    """
    def alwaysdata_setup(self):
        """
        adds the configuration file
        """
        filename = 'django.fcgi'
        fcgi_origin = '/'.join(env.conf_template.split('/')[:-1]+[filename])
        fcgi_destiny = '/'.join(env.wsgi_path.split('/')[:-1]+[filename])
#        put(fcgi_origin,fcgi_destiny)
        run("chmod +x %s" % fcgi_destiny)
