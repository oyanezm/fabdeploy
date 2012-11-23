from fabric.api import settings, sudo, env
from fabric.contrib import django
from django.conf import settings as django_settings

class _DatabaseSetup(object):
    """
    setup the database for deployment. Dev Only
    """

    def setup_database(self):
        """
        Setup the user and db in postgre
        """
        print "Creating role and database"
        self.drop_database()
        self.drop_user()
        self.create_user()
        self.create_database()

    def drop_database(self):
        """
        drops project and test database
        """
        with settings(warn_only = True):
            sudo('psql -c "DROP DATABASE %s"' % env.db_table, user='postgres')
            sudo('psql -c "DROP DATABASE test_%s"' % env.db_table, user='postgres')

    def drop_user(self):
        """
        deletes a user in the database
        """
        with settings(warn_only = True):
            sudo('psql -c "DROP ROLE %s"' % env.db_user, user='postgres')

    def create_user(self):
        """
        Creates a role in the db
        """
        with settings(warn_only = True):
            sudo('psql -c "CREATE USER %s WITH CREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"'
                % (env.db_user, env.db_pass), user='postgres')

    def create_database(self):
        """
        Creates the database
        """
        # creates user
        with settings(warn_only = True):
            sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"'
                % (env.db_table, env.db_user), user='postgres')
