from fabric.api import task, env
from pdb import set_trace as brake

def setup():
    """
    user and db  setup in postgre
    """
    print "Creating role and database"
    drop_database()
    drop_user()
    create_user()
    create_database()

@task
def backup():
    """
    backups db (mysql only)
    """
    from fabdeploy import app

    # dump sql in backup folder
    dump()
    app.backup_to_gzip()

def dump():
    """
    Dumps the database in the backup folder
    """
    from fabric.api import settings, sudo, env, task, run
    import datetime

    # remove old backup folder and create new one
    print("\nCleaning Old Backup for " + str(datetime.date.today()))
    with settings(warn_only = True):
        run('rm -rf ' + env.today_backup_gzip)
        run('rm -rf ' + env.today_backup_folder)
        run('mkdir '  + env.today_backup_folder)

    # Dump File
    print("\nDumping Database")
    filename = "dump.sql";
    today_backup_sql = env.today_backup_folder + '/' + filename
    with settings(warn_only = True):
        # dump sql with or withour password
        if env.db_pass: query = 'mysqldump -u %s -p %s > %s ';
        else:               query = 'mysqldump -u %s %s > %s ';
        sudo(query % (env.db_user,env.db_name,today_backup_sql));

def drop_database():
    """
    drops project and test database
    """
    from fabric.api import settings,sudo,env
    with settings(warn_only = True):
        sudo('psql -c "DROP DATABASE %s"' % env.db_name, user='postgres')
        sudo('psql -c "DROP DATABASE test_%s"' % env.db_name, user='postgres')
        sudo('psql -c "DROP DATABASE test_%s"' % env.db_name, user='postgres')


def drop_user():
    """
    deletes a user in the database
    """
    from fabric.api import settings,sudo,env
    with settings(warn_only = True):
        sudo('psql -c "DROP ROLE %s"' % env.db_user, user='postgres')

def create_user():
    """
    Creates a role in the db
    """
    from fabric.api import settings,sudo,env
    with settings(warn_only = True):
        sudo('psql -c "CREATE USER %s WITH CREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"'
            % (env.db_user, env.db_pass), user='postgres')

def create_database():
    """
    Creates the database
    """
    from fabric.api import settings,sudo,env
    # creates user
    with settings(warn_only = True):
        sudo('psql -c "CREATE DATABASE %s WITH OWNER %s"'
            % (env.db_name, env.db_user), user='postgres')
