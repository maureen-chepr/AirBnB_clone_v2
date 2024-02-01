#!/usr/bin/python3
"""
    script that distributes an archive to your web servers
"""
import os.path
from datetime import datetime
from fabric.api import *

env.hosts = ['100.26.254.70', '34.201.174.4']


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if os.path.exists(archive_path) is False:
        return False
    archive_name = archive_path.split('/')[1]
    archive_name_mod = archive_name.split(".")[0]
    remote_path = "/data/web_static/releases/" + archive_name_mod
    upload_path = "/tmp/" + archive_name
    put(archive_path, upload_path)
    run('mkdir -p' + remote_path)
    run('tar -xzf /tmp/{} -C {}/'.format(archive_name, remote_path))
    run('rm {}'.format(upload_path))
    move = 'mv ' + remote_path + '/web_static/* ' + remote_path + '/'
    run(move)
    run('rm -rf ' + remote_path + '/web_static')
    run('rm -rf /data/web_static/current')
    run('ln -s ' + remote_path + ' /data/web_static/current')
    return True
