# -*- coding: utf-8 -*-
import os
import sys

os.chdir("template")
sys.path.append(os.getcwd())

import main_frame.main as main
main.Main(['main_frame/main.py', 'conf/conf.conf'])
