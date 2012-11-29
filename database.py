from fabric.api import settings, sudo, env, task
from fabric.contrib import django

@task
def setup():
    """
    user and db  setup in postgre
    """
    print "Creating role and database"
    drop_database()
    drop_user()
    create_user()
    create_database()

def drop_database():
    """
    drops project and test database
    """
    with settings(warn_only = True):
        sudo('psql -c "DROP DATABASE %s"' % env.db_table, user='postgres')
        sudo('psql -c "DROP DATABASE test_%s"' % env.db_table, user='postgres')

def drop_user():
    """
    deletes a user in the database
    """
    with settings(warn_only = True):
        sudo('psql -c "DROP ROLE %s"' % env.db_user, user='postgres')

def create_user():
    """
    Creates a role in the db
    """
    with settings(warn_only = True):
        sudo('psql -c "CREATE USER %s WITH CREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"'
            % (env.db_user, env.db_pass), user='postgres')

def create_database():
    """
    Creates the database
    """
    # creates user
    with settings(warn_only = True):
        sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"'
            % (env.db_table, env.db_user), user='postgres')
