# -*- coding: utf-8 -*-
__author__ = 'eternnoir'

import os
from subprocess import Popen, PIPE


class Nuget(object):
    def __init__(self, nuget_path="./.nuget/NuGet.exe", debug = False):
        self.exe_path = nuget_path
        self.debug = debug

    def restore(self, solution_filepath, *opts):
        if not os.path.isfile(self.exe_path):
            raise Exception("Nuget.exe not found at " + self.exe_path)
        command = [self.exe_path, "restore", solution_filepath]
        for par in opts:
            command.append(par)
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if self.debug:
            print(output)
            print(err)
        if p.returncode == 1:
            return False
        return True
