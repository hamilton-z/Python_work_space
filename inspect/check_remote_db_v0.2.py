#-*- coding: utf-8 -*-
import sys
import argparse

import configparser
import pyodbc
from bak.inspect.test import time


def cmd_Line():
    parser = argparse.ArgumentParser(description='This is a program,use to run database command and log the result')
    parser.add_argument('-c','--config',dest='file',help='The config file path and name',default='config.ini')
    parser.add_argument('-l','--log',dest='logfile',help='The log file path and name',default='db_check_log.txt')
    args = parser.parse_args()
    return args

    
def config_Read(file):
    
    defaults = []
    dbs = []
    
    config = configparser.ConfigParser(strict=False)
    config.read(file)

    dbtype = config.get("public","dbtype")
    defaults.append(dbtype)

    dbdriver = config.get("public","dbdriver")
    defaults.append(dbdriver)
    
    database = config.get("public","database")
    defaults.append(database)
    
    port = config.get("public","port")
    defaults.append(port)
    
    user = config.get("public","user")
    defaults.append(user)
    
    passwd = config.get("public","passwd")
    defaults.append(passwd)
    
    cmd = config.get("public","cmd")
    defaults.append(cmd)
    
    secs = config.sections()
    for items in secs[1:]:
        dbs.append(items)
        value = []
 
        dbtype_items = config.get(items,"dbtype")
        value.append(dbtype_items)
                       
        dbdriver_items = config.get(items,"dbdriver")
        value.append(dbdriver_items)
        
        database_items = config.get(items,"database")
        value.append(database_items)
        
        port_items = config.get(items,"port")
        value.append(port_items)
        
        user_items = config.get(items,"user")
        value.append(user_items)
        
        passwd_items = config.get(items,"passwd")
        value.append(passwd_items)
        
        cmd_items = config.get(items,"cmd")
        value.append(cmd_items)
        for i in range(len(value)):
            if not value[i]:
                value[i]=defaults[i]
                print(value[i])
                i += 1      
        dbs.extend(value)
    return dbs

def conn_Dbs(machine,files):

    num = len(machine)
    sql_list = []
    print("This is database connection module")
    for i in range(0,num,8):
        hostname=str(machine[i]).strip()
        i += 1
        dbtype=str(machine[i]).strip()
        i += 1
        dbdriver=str(machine[i]).strip()
        i += 1
        database=str(machine[i]).strip()
        i += 1
        port=str(machine[i]).strip()
        i += 1
        username=str(machine[i]).strip()
        i += 1
        password=str(machine[i]).strip()
        i += 1
        sqls = str(machine[i]).strip()
        sql_list=sqls.split(";")
        if dbtype == "mysql":
            conn_info = ('Driver={%s};Server=%s;Database=%s;User=%s; Password=%s;Option=3;' %(dbdriver, hostname, database, username, password ))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        elif dbtype == "pg":
            conn_info = ('Driver={%s};Server=%s;Port=%d;Database=%s;Uid=%s;Pwd=%s;' %(dbdriver, hostname, int(port), database, username, password ))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        elif dbtype == "oracle":
            conn_info = ('Driver={%s};CONNECTSTRING=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=%s)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=%s)));Uid=%s;Pwd=%s;' %(dbdriver, hostname, database, username, password))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        elif dbtype == "sybase":
            conn_info = ('Driver={%s};server=%s;db=%s;uid=%s;pwd=%s;port=%d;language=us_english;' %(dbdriver, hostname, database, username, password,int(port)))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        elif dbtype == "db2":
            conn_info = ('Driver={%s};Hostname=%s;Database=%s;Port=%d;Protocol=TCPIP;Uid=%s;Pwd=%s;' %(dbdriver, hostname, database, int(port), username, password))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        elif dbtype == "ms":
            conn_info = ('Driver={%s};Server=%s;Database=%s;Uid=%s;Pwd=%s;' %(dbdriver, hostname, database, username, password))
            print("\n=====================\n%s\n=====================" % hostname)
            print("Now useing %s....." % dbdriver)
        else:
            print("\n=====================\n%s\n=====================" % hostname)
            print("Your Database do not support in this program!\n Contact the Programer")
    
        try:
            db_con = pyodbc.connect(conn_info)
            db_cur = db_con.cursor()
            for sql in sql_list:
                print("\n================\n%s\n================\n" % sql)
                db_cur.execute(sql)
                records = db_cur.fetchall()
                for record in records:
                    timers = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(test.zjb.time()))
                    print(timers+'---'+str(record))
                
            db_con.close
                    
        except Exception as e: 
                    print(e)
                    print("\n=====================\nFinished\n=====================")
                    
        if '-l' in sys.argv[:] :
            filehandle = open(files,'a')
            try:
                filehandle.write('\n=======================\n====>>'+hostname+'\n=======================\n\n'+timers+'\n')
                for sql in sql_list:
                    filehandle.write('\n============================\n====>>'+sql+'\n============================\n')
                    for record in records:
                        filehandle.write('\n'+str(record)+'\n')
                filehandle.write('\n=======================\n====>>finished\n=======================\n\n'+timers+'\n')
            finally:
                filehandle.close()
                
                
if __name__ == '__main__': 
    args = cmd_Line()
    machine = config_Read(args.file)
    files = args.logfile
    conn_Dbs(machine,files)
