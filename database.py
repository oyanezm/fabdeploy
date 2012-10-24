from fabric.api import settings, sudo, env
from fabric.contrib import django
from django.conf import settings as django_settings

#TODO: put this validation somewhere else
# avoids "fab -l" to fail.
if('settings_package' not in env):
    from deploy.lib.helper import _AttrDict
    django_settings = _AttrDict(DB_USER = '',
                                DB_PASSWORD = '',
                                DB_NAME = '')
else:
    django.settings_module(env.settings_package)

class _DatabaseSetup(object):
    """
    setup the database for deployment. Dev Only
    """
    db_user = django_settings.DB_USER
    db_pass = django_settings.DB_PASSWORD
    db_table = django_settings.DB_NAME

    def setupdb(self):
        """
        Setup the user and db in postgre
        """
        print "Creating role and database"
        self.drop_user()
        self.create_user()
        self.resetdb()

    def drop_user(self):
        """
        deletes a user in the database
        """
        with settings(warn_only = True):
            sudo('psql -c "DROP DATABASE %s"' % self.db_table, user='postgres')
            sudo('psql -c "DROP DATABASE test_%s"' % self.db_table, user='postgres')
            sudo('psql -c "DROP ROLE %s"' % self.db_user, user='postgres')

    def create_user(self):
        """
        Creates a role in the db
        """
        with settings(warn_only = True):
            sudo('psql -c "CREATE USER %s WITH CREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"'
                % (self.db_user, self.db_pass), user='postgres')

    def resetdb(self):
        """Creates role and database"""
        # creates user
        with settings(warn_only = True):
            sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"'
                % (self.db_table, self.db_user), user='postgres')
        print "db reset done!"
