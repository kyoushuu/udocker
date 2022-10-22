# -*- coding: utf-8 -*-
"""PRoot management"""

import sys
import os

from msg import Msg
from config import Config
from helper.hostinfo import HostInfo
from utils.fileutil import FileUtil


class PRoot(object):
    """Set proot executable
    """

    def __init__(self, localrepo):
        self.localrepo = localrepo
        self.executable = None                   # PRoot

    def select_proot(self):
        """Set proot executable"""
        self.executable = Config.conf['use_proot_executable']
        if self.executable != "UDOCKER" and not self.executable:
            self.executable = FileUtil("proot").find_exec()

        if self.executable == "UDOCKER" or not self.executable:
            self.executable = ""
            arch = HostInfo().arch()
            image_list = []
            if arch == "amd64":
                if HostInfo().oskernel_isgreater([4, 8, 0]):
                    image_list = ["proot-x86_64-4_8_0", "proot-x86_64", "proot"]
                else:
                    image_list = ["proot-x86_64", "proot"]
            elif arch == "i386":
                if HostInfo().oskernel_isgreater([4, 8, 0]):
                    image_list = ["proot-x86-4_8_0", "proot-x86", "proot"]
                else:
                    image_list = ["proot-x86", "proot"]
            elif arch == "arm64":
                if HostInfo().oskernel_isgreater([4, 8, 0]):
                    image_list = ["proot-arm64-4_8_0", "proot-arm64", "proot"]
                else:
                    image_list = ["proot-arm64", "proot"]
            elif arch == "arm":
                if HostInfo().oskernel_isgreater([4, 8, 0]):
                    image_list = ["proot-arm-4_8_0", "proot-arm", "proot"]
                else:
                    image_list = ["proot-arm", "proot"]
            f_util = FileUtil(self.localrepo.bindir)
            self.executable = f_util.find_file_in_dir(image_list)

        if not os.path.exists(self.executable):
            Msg().err("Error: proot executable not found")
            sys.exit(1)

        return self.executable
