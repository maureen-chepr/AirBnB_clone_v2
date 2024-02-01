#!/usr/bin/python3
"""
    Deletes out-of-date archives
"""
from fabric.api import *
import os

env.hosts = ['100.26.254.70', '34.201.174.4']

def do_clean(number=0):
    """
    Deletes unnecessary archives in the versions and /data/web_static/releases folders
    """
    number = int(number)
    if number < 0:
        return

    # Local cleanup (versions folder)
    local_arch = local('ls -1t versions | grep .tgz | tail -n +{}'.format(number + 1), capture=True)
    with lcd('versions'):
        for archive in local_arch.split('\n'):
            local('rm -f {}'.format(archive))

    # Remote cleanup (web servers)
    remote_archives = run('ls -1t /data/web_static/releases | grep web_static_ | tail -n +{}'.format(number + 1))
    for archive in remote_archives.split('\n'):
        if archive.strip() != "":
            with cd('/data/web_static/releases'):
                run('rm -rf {}'.format(archive))
