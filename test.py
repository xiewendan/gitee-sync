# -*- coding: utf-8 -*-
import os
import sys

os.chdir("template")
sys.path.append(os.getcwd())

import unit_test.run_test as run_test
run_test.Main()

import main_frame.main as main
main.Main(['main_frame/main.py', 'conf/conf.conf'])
