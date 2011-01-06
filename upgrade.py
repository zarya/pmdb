import MySQLdb
import CommandLineApp
import os
import sys
import re
from datetime import datetime
import hashlib
from subprocess import Popen, PIPE

DB_NAME = ''
DB_HOST = ''
DB_USER = ''
DB_PASS = ''

reSQL = re.compile(";\s*$", re.MULTILINE)

db_connection = MySQLdb.connect(host=DB_HOST, 
                                db=DB_NAME, 
                                user=DB_USER, 
                                passwd=DB_PASS)


def get_version_list():
    c = db_connection.cursor()
    query = """select distinct version, svn_version 
                 from versions
             order by version;"""
    count = c.execute(query)
    versions = []
    if count > 0:
        versions = [version for version in c.fetchall()]
    return versions
    

class upgrade(CommandLineApp.CommandLineApp):
    """Upgrades the website database."""
    
    EXAMPLES_DESCRIPTION = """
To execute all scripts within a directory:

  $ upgrade --execute --dir /path/to/sqlscripts
  
To execute only some scripts within a directory:

  $ upgrade --execute --dir /path/to/sqlscripts 2008*
  
To just print out script, but don't execute:

  $ upgrade --dir /path/to/sqlscripts 2008*

To just print out scripts in the current working directory, 
but don't execute:

  $ upgrade

To execute all scripts in the current working directory:

  $ upgrade --execute
"""
    def __init__(self, commandLineOptions=sys.argv[1:]):
        super(upgrade, self).__init__(commandLineOptions=sys.argv[1:])
        
    execute = False
    def optionHandler_execute(self):
        """Turn on the excution option.  Defaults to False."""
        self.execute = True
        return
    
    dir = os.getcwd()
    def optionHandler_dir(self, name):
        """Set the directory that contains the scripts to execute.  
        Defaults to current working directory."""
        self.dir = name
        return
        
    def filter_down(self, *cherries):
        already_applied = get_version_list()
        print "# ALREADY APPLIED:"
        for x in already_applied:
            print '#\t%s\tr%s' % (x[0], x[1])
        in_directory = os.listdir(self.dir)
        in_directory.sort()
        sql_in_directory = []
        for sql in in_directory:
            if os.path.splitext(sql)[-1] == '.sql':
                sql_in_directory.append(sql)
        to_execute = []
        if cherries:
            for cherry in cherries:
                if cherry not in already_applied:
                    if cherry[0] in sql_in_directory:
                        to_execute.append(cherry[0])
        else:
            for sql in sql_in_directory:
                if sql not in [info[0] for info in already_applied]:
                    to_execute.append(sql)
        print '# TO EXECUTE:'
        for x in to_execute:
            print '#\t%s' % x
        return to_execute
        
    def get_rev(self, sql):
        svninfo = Popen(["svn", "info", sql], stdout=PIPE).stdout.readlines()
        for info in svninfo:
            tokens = info.split(':')
            if tokens[0].strip() == 'Last Changed Rev':
                return tokens[1].strip()
        return 0
        
    def split_file(self, sql):
        full_path = os.path.join(self.dir, sql)
        contents = open(full_path, 'r').read()
        size = os.stat(full_path).st_size
        sha1 = hashlib.sha1(contents).hexdigest()
        rev = self.get_rev(full_path)
        print "## Processing %s, %s bytes, sha1 %s, svn rev %s" % \
                (sql, size, sha1, rev)
        return {
            'statements':reSQL.split(contents), 
            'full_path':full_path, 
            'contents':contents, 
            'size':size, 
            'sha1':sha1, 
            'rev':rev
        }
        
    def execute_sql(self, statement, segment_number):
        segment = (
            segment_number, 
            len(statement), 
            hashlib.sha1(statement).hexdigest()
        )
        if not self.execute:
            print "### printing segment %s, %s bytes, sha1 %s" % segment
            print "%s;" % statement
        if self.execute:
            print "### executing segment %s, %s bytes, sha1 %s" % segment
            print "%s;" % statement
            c = db_connection.cursor()
            count = c.execute(statement)
            print "### SUCCESS, %s rows affected." % count
            return True
        return True
        
    def stamp_database(self, sql, statements, svn):
        print "## DB status updated: %s" % sql
        if self.execute:
            c = db_connection.cursor()
            count = c.execute("""
INSERT INTO versions (version, date_created, sql_executed, svn_version) 
VALUES (%(sql)s, %(date)s, %(statements)s, %(revision)s);""", {
    'sql':sql, 
    'date':datetime.now(), 
    'statements':';\n'.join(statements)+';', 
    'revision':svn
            })       
    
    def main(self, *args):
        print "# Script began %s" % datetime.now()
        to_execute = self.filter_down(*args)
        for sql in to_execute:
            split_data = self.split_file(sql)
            statements = split_data['statements']
            executed_stmts = []
            segment_num = 0
            for statement in  statements:
                stmt = statement.strip()
                if stmt and stmt not in ('BEGIN', 'COMMIT',) and \
                    "UPDATE `version` SET `serial_number`" not in stmt:
                    if self.execute_sql(stmt, segment_num):
                        executed_stmts.append(stmt)
                segment_num += 1
            # for each file update the database version
            self.stamp_database(sql, executed_stmts, split_data['rev'])
            print "-"*70
        print "# Script ended %s" % datetime.now()
        
        
if __name__ == "__main__":
    up = upgrade()
    up.run()
