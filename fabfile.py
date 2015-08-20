# -*- coding: utf-8 -*-

from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration

env.user="www-data"
env.hosts = ["chtoes.li"]
path = {
        "dev": '/var/www/dev.xkcd.ru/public/',
        "prod": '/var/www/xkcd.ru/public/',
        }

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build(environment):
    local('pelican -q -s pelicanconf-{}.py'.format(environment))

def rebuild(environment):
    clean()
    build(environment)

def regenerate(environment):
    local('pelican -q -r -s pelicanconf-{}.py'.format(environment))

def serve():
    local('cd {deploy_path} && python2 -m SimpleHTTPServer'.format(**env))

def reserve(environment):
    build(environment)
    serve()

def preview(environment):
    local('pelican -s pelicanconf-{}.py'.format(environment))

def publish(environment):
    local('pelican -q -s pelicanconf-{}.py'.format(environment))
    project.rsync_project(
        remote_dir=path[environment],
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
