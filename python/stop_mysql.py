#stop_mysql.py

import os, sys, getopt, urllib, tarfile, MySQLdb, string, time
from   optparse import OptionParser

def parse_parameter(argv):

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", default="4337", help="port mysql started")
    parser.add_option("-b", "--base-dir", dest="base_dir", default="./mysql", help="dir mysql installed")
    parser.add_option("-d", "--data-dir", dest="data_dir", default="./data", help="dir mysql data stored")
    (options, args) = parser.parse_args()
    # change to absolute path
    options.base_dir = os.path.abspath(options.base_dir)
    options.data_dir = os.path.abspath(options.data_dir)
    return options

# start mysqld
def stop_mysqld(opt):
    print "Stopping mysql ..."

    mysql_bin = opt.base_dir + "/bin/mysqladmin shutdown"
    sock_file = opt.data_dir + "/mysqld.sock"

    stop_command = mysql_bin + " --socket=" + sock_file + " -u root"

    print stop_command

    os.system(stop_command)
    
    print "End stop mysql ..."

# create database table test needed
def clear_tables(opt):

    try:
        db = MySQLdb.connect(host="127.0.0.1", port=string.atoi(opt.port), db="test")
        cursor = db.cursor()
        # drop table if existed
        cursor.execute("DROP TABLE IF EXISTS Pool")
        cursor.execute("DROP TABLE IF EXISTS User")

        db.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def main(argv):

    # parse parameters
    opt = parse_parameter(argv)
    
    # clear mysql tables
    clear_tables(opt)

    # stop mysqld
    stop_mysqld(opt)

if __name__ == "__main__":
    main(sys.argv[1:])
