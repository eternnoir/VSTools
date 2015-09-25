# -*- coding: utf-8 -*-
__author__ = 'eternnoir'

import os
from subprocess import Popen, PIPE


class MsBuild:
    def __init__(self, msBuildPath, debug=False):
        self.executePath = msBuildPath
        self.debug = debug

    def build(self, slnPath, *paras):
        if not os.path.isfile(self.executePath):
            raise Exception("MsBuild.exe not found at " + self.executePath)
        command = [self.executePath, slnPath]
        for par in paras:
            command.append(par)
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if self.debug:
            print(output)
        if p.returncode == 1:
            return False
        return True
    def build_release(self, sln_path):
        return self.build_release_target(sln_path)

    def build_release_target(self, sln_path, target=None):
        arg1 = '/t:Rebuild'
        arg2 = '/p:Configuration=Release'
        if target is None:
            return self.build(sln_path, arg1, arg2)
        else:
            arg3 = '/t:' + target
            return self.build(sln_path, arg1, arg2, arg3)
