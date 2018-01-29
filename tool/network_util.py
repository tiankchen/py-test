#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket


def hostname_to_ip(hostname):
    ip = socket.gethostbyname(hostname)
    return ip


def ip2hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        return hostname[0]
    except Exception, e:
        return ""


if __name__ == "__main__":
    hostname_array = ['www.baidu.com', 'www.qq.com']
    for hostname in hostname_array:
        print "{0}'s ip is: {1}".format(hostname, hostname_to_ip(hostname))

    ip_array = ['192.168.2.1', '192.168.2.2', '192.168.2.3']
    for ip in ip_array:
        print "{0}'s hostname is: {1}".format(ip, ip2hostname(ip))
