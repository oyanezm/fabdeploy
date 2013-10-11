from fabric.api import task
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
    from fabric.api import settings, sudo, env, task, run
    """
    backups db (mysql only)
    """
    import datetime
    today_date = str(datetime.date.today())
    today_backup_folder = env.backup_path + today_date
    today_backup_file = today_backup_folder + '.gz';

    # remove old backup folder and create new one
    print("Wipe Old Backup for "+today_date)
    with settings(warn_only = True):
        run('rm -rf ' + today_backup_file)
        run('rm -rf ' + today_backup_folder)
        run('mkdir ' + today_backup_folder)

    # Copy Site Folder
    print("Copy Site Folder")
    with settings(warn_only = True):
        run('cp -r ' + env.path +' '+today_backup_folder)

    # Dump File
    print("Dump Database")
    filename = "dump.sql";
    today_backup_sql = today_backup_folder + '/' + filename
    with settings(warn_only = True):
        # dump sql with or withour password
        if env.db_pass: query = 'mysqldump -u %s -p %s > %s ';
        else:               query = 'mysqldump -u %s %s > %s ';
        sudo(query % (env.db_user,env.db_name,today_backup_sql));


    print("Gzip and Clean")
    # Gzip folder and remove
    with settings(warn_only = True):
        # no output on both TODO: Fix path on gziped file
        run('tar -czf %s %s >/dev/null 2>&1' % (today_backup_file, today_backup_folder))
        run('rm -rf ' + today_backup_folder + ' 2> /dev/null')

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
