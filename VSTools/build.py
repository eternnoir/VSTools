#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

__author__ = 'eternnoir'

import os


class MsBuild:
    def __init__(self, msBuildPath, debug=False):
        self.executePath = msBuildPath
        self.debug = debug

    def build(self, slnPath, *para):
        if not os.path.isfile(self.executePath):
            raise Exception("MsBuild.exe not found at " + self.executePath)
        print(self.executePath)
        print(slnPath)
        p = subprocess.call([self.executePath, slnPath, para])
        if p == 1:
            return False
        return True
