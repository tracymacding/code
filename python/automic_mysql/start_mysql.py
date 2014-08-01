# start_mysql.py

import os, sys, getopt, urllib, tarfile, MySQLdb, string, time
from   optparse import OptionParser

# parse parameters, return as option
def parse_parameter(argv):

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", default="4338", help="port mysql started")
    parser.add_option("-d", "--dir", dest="dir", default="/tmp", help="dir mysql installed")
    (options, args) = parser.parse_args()
    # change to absolute path
    options.dir = os.path.abspath(options.dir)
    return options

# download mysql.xx-xx.tar.gz to /tmp/
def download_mysql(url):
    print "Downloading mysql tar ..."

    i = url.rfind('/')
    file = url[i+1:]
    dest = "/tmp/" + file
    if os.path.exists(dest):
        print "Skipping download, file existed"
        return dest

    print url, "-->", dest
    # TODO: we should judge here
    urllib.urlretrieve(url, dest)

    print "End download mysql tar ..."
    return dest

# tar -zxvf mysql.xx.xx.tar.gz to dest dir
def tar_mysql(file, opt):
    print "Untar mysql tar ..."

    tar = tarfile.open(file)
    names = tar.getnames()
    idx = 0
    for name in names:
        if idx == 0:
            mysql_dir = opt.dir + "/" + name
            if os.path.exists(mysql_dir):
                print "Skipping untar, already exist ... "
                return mysql_dir

        tar.extract(name, path=opt.dir)
        idx = idx + 1

    tar.close()

    print "Untar mysql tar to ", mysql_dir
    print "End untar mysql tar ..."

    return mysql_dir

def install_mysql(opt, base_dir):
    print "Installing mysql ..."

    data_dir = base_dir + "/data"

    install_command = base_dir + "/bin/mysql_install_db" + " --basedir=" + base_dir + " --datadir=" + data_dir + " --user=hzdingkai2013"
    os.system(install_command)
    print "End installing mysql ..."

def generate_config_file(opt, base_dir):
    
    print "Generating mysql confile file ..."
    config_file = base_dir + "/data/my.conf"
    print "Mysql confile file: ", config_file

    f = open(config_file, 'w')

    headc = "[client]\n"
    port = "port = " + opt.port + "\n"
    socket = "socket = " + base_dir + "/data/mysqld.sock\n"
    heads = "[mysqld_safe]\n"
    user = "user = hzdingkai2013\n"
    ledir = "ledir = " + base_dir + "/bin\n"
    headd = "[mysqld]\n"
    bind_address = "bind-address = 127.0.0.1\n"
    pid = "pid-file = " + base_dir + "/data/mysqld.pid\n"
    data_dir = "datadir = " + base_dir + "/data\n"
    base_dir_s = "basedir = " + base_dir + "\n"
    log_error = "log-error = " + base_dir + "/data/mysqld.log\n"
    lc_mess = "lc-messages-dir = " + base_dir + "/share"

    f.write(heads)
    f.write(user)
    f.write(ledir)
    f.write(headd)
    f.write(bind_address)
    f.write(port)
    f.write(pid)
    f.write(socket)
    f.write(base_dir_s)
    f.write(data_dir)
    f.write(log_error)
    f.write(user)
    f.write(lc_mess)

    f.close()

    print "End generate mysql confile file ..."
    return config_file

# start mysqld
def start_mysqld(opt, base_dir):
    print "Starting mysql ..."

    mysql_bin = base_dir + "/bin/mysqld_safe"
    config_file = generate_config_file(opt, base_dir)

    start_command = mysql_bin + " --defaults-file=" + config_file + " &"

    print start_command

    os.system(start_command)
    
    print "End starting mysql ..."

# create database table test needed
def create_tables(opt):

    try:
        db = MySQLdb.connect(host="127.0.0.1", port=string.atoi(opt.port), db="test")
        cursor = db.cursor()
        # drop table if existed
        print "Create table Pool ..."
        #cursor.execute("DROP TABLE Pool")
        sql = """CREATE TABLE Pool (
             PoolID  bigint not null primary key,
             PoolName  varchar(256) not null)"""
        cursor.execute(sql)

        print "Create table User ..."
        #cursor.execute("DROP TABLE User")
        sql = """CREATE TABLE User (
             UID  bigint not null primary key,
             Name  varchar(256) not null,
             Passwd    varchar(256) not null,
             PoolID  bigint not null,
             AllocPolicy blob not null)"""
        cursor.execute(sql)

        print "Create table Whitelist ..."
        #cursor.execute("DROP TABLE Whitelist")
        sql = """CREATE TABLE Whitelist (
             IP  varchar(32) not null primary key)"""
        cursor.execute(sql)

        print "Create table Zone ..."
        sql = """CREATE TABLE Zone (
             ZoneID  bigint not null primary key,
             PoolID  bigint not null)"""
        cursor.execute(sql)

        print "Create table PS ..."
        sql = """CREATE TABLE PS (
             PSID   bigint not null primary key,
             IP     varchar(32) not null,
             Zone   bigint not null,
             Token  bigint not null,
             DiskType tinyint not null,
             Capacity bigint not null,
             Free     bigint not null,
             ReadOnly tinyint not null,
             Fs       varchar(32) not null,
             Mounted  varchar(256) not null)"""
        cursor.execute(sql)

        print "Create table Partition ..."
        sql = """CREATE TABLE Partition (
             PID         bigint not null primary key,
             Epoch       bigint not null,
             Size        bigint not null,
             Free        bigint not null,
             Type        tinyint not null,
             ReadOnly    tinyint not null,
             AllocPolicy tinyint not null,
             Replication blob not null)"""
        cursor.execute(sql)

        db.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def main(argv):

    url = "http://db-11.space.163.org/mysql-5.5.20-v3i-linux-x86_64.tar.gz"

    # parse parameters
    opt = parse_parameter(argv)

    # download mysql.tar to dir passed by parameter
    dest = download_mysql(url)

    # tar -zxvf 
    mysql_dir = tar_mysql(dest, opt)

    # install mysql
    install_mysql(opt, mysql_dir)
    
    # start mysqld
    start_mysqld(opt, mysql_dir)

    print "Waitting 10 seconds, mysql to start ..."
    time.sleep(10)

    # create table
    create_tables(opt)

if __name__ == "__main__":
    main(sys.argv[1:])
