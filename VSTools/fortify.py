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

    def scan(self, build_id, path, output_frp, pdf_filename=None, need_clean=True, load_dlls=True):
        self.__check_sca_bin__()
        if need_clean:
            self.__print__("Start Clean.")
            r, output = self.clean(build_id, path)
            if not r:
                self.__print__(output)
                raise Exception("Clean Fail.")

        dll_args = []
        if load_dlls:
            dll_args = self.__build_dll_args__(path)

        self.__print__("Start Translating.")
        r, output = self.translating(build_id, path, args=dll_args)
        self.__print__(output)
        if not r:
            raise Exception("Transtating Fail.")

        self.__print__("Start Scan.")
        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id, '-scan',
                   '-f', output_frp]
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        self.__print__(output)
        self.__print__(err)
        if p.returncode != 0:
            return False, output
        return True, output

    def translating(self, build_id, path, args=[]):
        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id]
        for arg in args:
            command.append(arg)
        command.append(os.path.abspath(path))
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=path)
        output, err = p.communicate()
        self.__print__(output)
        self.__print__(err)
        if p.returncode != 0:
            return False, output
        return True, output

    def clean(self, build_id, path):
        command = [self.bin_path, self.__build_max_memory_command__(), self.__build_min_memory_command__(),
                   '-vsversion', self.vs_version, '-b', build_id, '-clean']
        p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=path)
        output, err = p.communicate()
        self.__print__(output)
        self.__print__(err)
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

    def __build_dll_args__(self, folder_path):
        ret = ["-libdirs"]
        dll_list = get_all_dll_path(folder_path)
        if len(dll_list) == 0:
            return []

        dll_path_string = ""
        for dll_path in dll_list:
            dll_path_string += dll_path + ";"

        ret.append(dll_path_string)
        return ret

    def __print__(self, message):
        if self.debug:
            print(message)


def get_all_dll_path(folder_path):
    ret = []
    import os
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".dll"):
                ret.append(os.path.abspath(os.path.join(root, file)))
    return ret