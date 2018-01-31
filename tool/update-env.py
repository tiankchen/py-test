#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import shutil
import time
import subprocess
from ConfigParser import ConfigParser


class Node:
    section_name = ''
    item_name = ''

    def __init__(self, section_name, item_name):
        self.section_name = section_name
        self.item_name = item_name


# noinspection PyMethodMayBeStatic
class UpdateConfig:
    YES = "yes"

    # configuration file path
    config_path = ''

    key_dict = {"yum-repo-163": "update-env",
                "yum-repo-epel": "update-env"}
    config_dict = {}

    def __init__(self, config_path):
        self.config_path = config_path
        pass

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise IOError("Config file: '%s' not exists." % self.config_path)

        parser = ConfigParser()
        parser.read(self.config_path)

        keys = self.key_dict.keys()
        for key in keys:
            section = self.key_dict[key]
            try:
                value = parser.get(section, key)
                self.config_dict[key] = value
                print "Load '%s:%s' success: %s" % (section, key, value)
            except Exception, e:
                print "Load '%s:%s' failed: %s" % (section, key, e)

    def update_env(self):
        self.update_yum()

        shell_commands = ['yum install -y lrzsz', ]
        for command in shell_commands:
            self.execute_shell_command(command)

    def update_yum(self):
        if self.need_update_163_repo():
            print "## Update yum repo from www.163.com ..."
            self.sleep()

            repo_file = 'resources/CentOS6-Base-163.repo'
            dst_file = '/etc/yum.repos.d/CentOS6-Base-163.repo'
            self.check_file_exists(repo_file)

            print "copy '%s' to '%s'" % (repo_file, dst_file)
            shutil.copy(repo_file, dst_file)

    def need_update_163_repo(self):
        return self.config_dict["yum-repo-163"] == self.YES

    def check_file_exists(self, path):
        if not os.path.exists(path):
            raise IOError("File '%s' is not exist." % path)

    def sleep(self, sec=1):
        time.sleep(sec)

    def execute_shell_command(self, command, args=[]):
        ret = subprocess.Popen(command, shell=True)


if __name__ == "__main__":
    config = UpdateConfig("update.cnf")
    config.load_config()

    config.update_env()
