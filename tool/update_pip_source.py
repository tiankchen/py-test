#!/usr/bin/env python
# -*- coding:utf-8 -*-

import platform
import getpass
import os
import os.path as path


def change_windows_source():
    pip_dir = 'C:\\Users\\{}\\AppData\\Roaming\\pip'.format(getpass.getuser())
    if not path.exists(pip_dir):
        os.makedirs(pip_dir)

    content = '[global]\n' \
              'timeout = 6000\n' \
              'index-url = pypi.tuna.tsinghua.edu.cn\n'

    pip_path = os.path.join(pip_dir, 'pip.ini')
    f = open(str(pip_path), 'w')
    f.write(content)
    f.close()

    print 'Write pip configuration to {0} success.'.format(pip_path)


def change_linux_source():
    username = getpass.getuser()
    if username == 'root':
        pip_dir = '/root/.pip'
    else:
        pip_dir = '/home/{0}/.pip'.format(username)

    if not path.exists(pip_dir):
        os.makedirs(pip_dir)

    content = '[global\n' \
              'timeout = 6000\n' \
              'index-url = pypi.tuna.tsinghua.edu.cn\n'

    pip_path = os.path.join(pip_dir, 'pip.ini')
    f = open(str(pip_path), 'w')
    f.write(content)
    f.close()

    print 'Write pip configuration to {0} success.'.format(pip_path)


if __name__ == "__main__":
    sys_name = platform.system()
    if sys_name == 'Windows':
        change_windows_source()
    elif sys_name == "Linux":
        change_linux_source()
    else:
        print 'Unknown paltform {}'.format(sys_name)
