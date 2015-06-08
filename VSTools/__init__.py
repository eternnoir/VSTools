#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eternnoir'
VERSION = "v0.0.1"

from VSTools.build import MsBuild
from subprocess import Popen, PIPE
import os

FrameworkVersionDic = {"v4.0.30319": r'C:\Windows\Microsoft.NET\Framework\v4.0.30319'}


def get_default_msbuild(debug=False):
    return MsBuild(FrameworkVersionDic["v4.0.30319"] + r'\MSBuild.exe', debug)


def deploy_copy(sourcepath, targetpath):
    if not os.path.isdir(sourcepath):
        raise Exception("Path :" + sourcepath + ". Not Found")
    if not os.path.isdir(targetpath):
        raise Exception("Path :" + targetpath + ". Not Found")
    command = ['xcopy', sourcepath, targetpath, '/D', '/K', '/E', '/Y', '/C', '/I', '/H']
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 1:
        return False
    return True

def stop_iis():
    command = ['iisreset', '/stop']
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 1:
        return False
    return True


def start_iis():
    command = ['iisreset', '/start']
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    if p.returncode == 1:
        return False
    return True

