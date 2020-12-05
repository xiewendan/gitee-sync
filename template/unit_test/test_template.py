# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 12:48

# desc:

import logging
import unittest

import main_frame.main as main


class TestAAA(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestCmdExcel2Py setUp:")

    # def test_fun(self):
        # main.Main(["main_frame/main.py", "excel2py", "config/excel", "config/setting"])

    def tearDown(self):
        logging.getLogger("myLog").debug("TestAAA tearDown\n\n\n")
