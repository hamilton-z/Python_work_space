#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import paramiko
import ConfigParser
import logging
import copy

def config_Read():
    host = {}
    info = {}
    config = ConfigParser.ConfigParser()
    config.read("ip_list_bak.txt")
    keys1 = config.options('public')
    for i in keys1:
        info[i] = config.get('public',i)
    ch1 = copy.deepcopy(info)
    ch2 = copy.deepcopy(info)
    ch1['cmd'] = ch1['cmd'].replace('lan print |', 'lan print 1 |',1)
    ch2['cmd'] = ch2['cmd'].replace('lan print |', 'lan print 8 |',1)
    keys2 = dict(config.items('IP'))
    for j in keys2.keys():
        if j == 'ch1':
            for ip in keys2[j].split(','):
                host[ip] = ch1
        elif j == 'ch8':
            for ip in keys2[j].split(','):
                host[ip] = ch2
    return host

def ssh(machine):
    sequ = 0
    #print "this is machine info: %s" % machine
    #print "This is ssh module"
    logger = initlog()
    for ip in machine.keys():
        hostname = ip
        port = int(machine[ip]['port'])
        username = machine[ip]['user']
        passwd = machine[ip]['passwd']
        cmds = machine[ip]['cmd'].split(';')
    
        # paramiko.util.log_to_file('runlog.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        #ssh.load_host_keys('/root/.ssh/known_hosts')
        try:
            logger.info('\n==================================\n====>>''第'+str(sequ)+'台'+'====>>'+hostname+'\n==================================\n')
            ssh.connect(hostname,port,username,passwd)
            for cmd in cmds:
                (stdin,stdout,stderr)=ssh.exec_command(cmd)
                output=stdout.read()
                logger.info('\n=======================\n====>>'+cmd+'\n=======================\n')
                logger.info(output)

        except socket.error:
            logger.info(hostname,'连接超时！')
            pass
        except paramiko.ssh_exception.AuthenticationException:
            logger.info(hostname,'验证失败，用户名或密码错误！')
        finally:
            ssh.close()
            logger.info('\n=======================\n====>>finished\n=======================\n\n')
        sequ += 1


def initlog():
    logging.basicConfig(level=logging.INFO,
                format='%(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)-8s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging


if __name__ == '__main__':

    iplist = config_Read()
    ssh(iplist)
