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
    pass


if __name__ == "__main__":
    # exe_cmd_on_remote()
    login_by_private_key()
