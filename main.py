#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko
import os
import platform
import getpass
import sys


# Execute command on the remote host
def exe_cmd_on_remote():
    hostname = '192.168.1.8'
    port = 22
    username = 'root'
    password = 'password'
    client = paramiko.SSHClient()  # 绑定实例
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, timeout=5)
    stdin, stdout, stderr = client.exec_command('df -sss')  # 执行bash命令
    result = stdout.read()
    error = stderr.read()

    # 判断stderr输出是否为空，为空则打印执行结果，不为空打印报错信息
    if not error:
        print result
    else:
        print error

    client.close()


# Login remote host by private key
def login_by_private_key():
    hostname = '192.168.1.8'
    port = 22
    username = 'root'
    key_file = ''
    command = "df -h"

    platform_name = platform.system()
    if platform_name == 'Windows':
        key_file = os.path.join('C:/', 'users', getpass.getuser(), '.ssh', 'id_rsa')
    elif platform_name == 'Linux':
        key_file = '~/.ssh/id_rsa'
    else:
        raise Exception('Unknown platform: %s' % platform_name)

    if not os.path.exists(key_file):
        raise IOError("File %s not exists." % key_file)

    client = paramiko.SSHClient()
    key = paramiko.RSAKey.from_private_key_file(key_file)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, pkey=key)
    stdin, stdout, stderr = client.exec_command(command)  # 标准输入，标准输出，错误输出
    result = stdout.read()
    error = stderr.read()
    if not error:
        print result
    else:
        print error

    client.close()


# upload file to remote host
def put_file():
    hostname = '192.168.1.8'
    port = 22
    username = 'root'
    password = 'password'
    local_path = 'main.py'
    remote_path = '/tmp/workspace/main.py'
    if not os.path.isfile(local_path):
        raise IOError('File %s not exists.' % local_path)

    try:
        s = paramiko.Transport((hostname, port))
        s.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(s)

        # 使用put()方法把本地文件上传到远程服务器
        sftp.put(local_path, remote_path)

        # 简单测试是否上传成功try:
        # 如果远程主机有这个文件则返回一个对象，否则抛出异常
        sftp.file(remote_path)
        print 'Put file %s success.' % local_path
    except IOError, e:
        print e
    except Exception, e:
        print e
    finally:
        s.close()


if __name__ == "__main__":
    # exe_cmd_on_remote()
    # login_by_private_key()
    put_file()
