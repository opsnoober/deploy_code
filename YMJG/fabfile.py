#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from fabric.api import *

# 登录用户和主机名：
env.user = 'secneo'
env.hosts = ['172.16.31.214'] # 如果有多个主机，fabric会自动依次部署
env.repo_scengine='git@192.168.138.66:sec/Pekingese/utility'
env.dir_scengine='utility'
env.branch_scengine='master'
env.tag_scengine='Pekingese_V1.2.2'
env.repo_server='git@192.168.138.66:sec/Pekingese/server'
env.dir_server='server'
env.branch_server='master'
env.tag_server='v1.0.0'

def pack_scengine():
    ' 定义一个pack任务 '
    # 打一个tar包：
    tar_files = 'scengine'
    local('rm -rf scengine.tgz %s'%env.dir_scengine)
    local('git clone %s'%env.repo_scengine)
    with lcd(env.dir_scengine):
        local('git checkout %s'%env.tag_scengine)
        local('tar -czvf ../scengine.tgz scengine')

def deploy_scengine():
    ' 定义一个部署任务 '
    # 远程服务器的临时文件：
    remote_tmp_tar = '~/deploy/scengine.tgz'
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    remote_dist_dir = '~/deploy/scengine@%s' % tag
    remote_back_dir = '~/deploy/scengine_backup'
    with settings(warn_only=True):
        run('rm -rf %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
        run('mkdir ~/deploy')
        put('scengine.tgz', remote_tmp_tar)
    # 解压：
        with cd('~/deploy'):
            run('mkdir %s' % remote_dist_dir)
            run('tar xvf scengine.tgz -C %s' % remote_dist_dir)
    # 备份
            run('mkdir %s' % remote_back_dir)
            run('cp -r /data/pek/scengine %s' % remote_back_dir)
    # 删除旧代码
            run('rm -rf /data/pek/scengine')
    # 拷贝新代码
            run('cp -r %s/scengine /data/pek/scengine' % remote_dist_dir)
    # 重启服务
            run('supervisorctl restart all')

def scengine():
    '部署scengine'
    pack_scengine()
    deploy_scengine()
