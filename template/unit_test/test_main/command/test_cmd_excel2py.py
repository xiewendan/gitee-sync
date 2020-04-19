# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/19 7:33 下午

# desc: 

import logging
import unittest

import main_frame.main as main


class TestCmdExcel2Py(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestCmdExcel2Py setUp:")

    def test_FileExt(self):
        main.Main(["run_test.py", "excel2py", "config/excel", "config/setting"])

    def tearDown(self):
        logging.getLogger("myLog").debug("TestCmdExcel2Py tearDown\n\n\n")
