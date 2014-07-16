#stop_mysql.py

import os, sys, getopt, urllib, tarfile, MySQLdb, string, time
from   optparse import OptionParser

def parse_parameter(argv):

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", default="4337", help="port mysql started")
    parser.add_option("-D", "--dir", dest="dir", default="/tmp", help="dir mysql installed")
    parser.add_option("-d", "--delete", dest="delete", default="false", help="delete everything after clear")
    (options, args) = parser.parse_args()
    # change to absolute path
    options.dir = os.path.abspath(options.dir)
    return options

# start mysqld
def stop_mysqld(opt):
    print "Stopping mysql ..."

    mysql_bin = opt.dir + "/bin/mysqladmin shutdown"
    sock_file = opt.dir + "/data/mysqld.sock"

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
        cursor.execute("DROP TABLE Pool")
        cursor.execute("DROP TABLE User")
        cursor.execute("DROP TABLE Whitelist")

        db.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def delete_everything(opt):
    if opt.delete == "true":
        delete_command = "rm -rf " + opt.dir
        os.system(delete_command)
        print "OK, i have delete the crime scene"

def main(argv):

    # parse parameters
    opt = parse_parameter(argv)
    
    # clear mysql tables
    clear_tables(opt)

    # stop mysqld
    stop_mysqld(opt)

    # delete installed dir if set
    delete_everything(opt)

if __name__ == "__main__":
    main(sys.argv[1:])
