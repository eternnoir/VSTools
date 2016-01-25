# -*- coding: utf-8 -*-
__author__ = 'eternnoir'

import os
from subprocess import Popen, PIPE

SOURCEANALYZERBIN = 'sourceanalyzer'


class FortifySCA(object):
    def __init__(self, bin_path=SOURCEANALYZERBIN, min_mem=400, max_mem=2048, vs_version='10.0', debug=False):
        self.vs_version = vs_version
        self.max_mem = max_mem
        self.min_mem = min_mem
        self.bin_path = bin_path
        self.debug = debug

    def scan(self, build_id, path, output_frp, pdf_filename=None, need_clean=True):
        self.__check_sca_bin__()
        if need_clean:
            r, output = self.clean(build_id, path)
            if not r:
                self.__print__(output)
                raise Exception("Clean Fail.")

        r, output = self.translating(build_id, path)
        self.__print__(output)
        if not r:
            raise Exception("Transtating Fail.")

        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id, '-scan',
                   '-f', output_frp]
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=path)
        output, err = p.communicate()
        if p.returncode != 0:
            return False, output
        return True, output

    def translating(self, build_id, path):
        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id, os.path.abspath(path)]
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=path)
        output, err = p.communicate()
        if p.returncode != 0:
            return False, output
        return True, output

    def clean(self, build_id, path):
        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id, '-clean']
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=path)
        output, err = p.communicate()
        if p.returncode != 0:
            return False, output
        return True, output

    def __check_parama__(self):
        if not self.__check_sca_bin__():
            raise Exception('SCA bin sourceanalyzer not found.')

    def __check_sca_bin__(self):
        command = [self.bin_path, '-h']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            print(output)
            return False

    def __build_max_memory_command__(self):
        return "-Xmx" + str(self.max_mem) + "M"

    def __build_min_memory_command__(self):
        return "-Xms" + str(self.min_mem) + "M"

    def __print__(self, message):
        if self.debug:
            print(message)
