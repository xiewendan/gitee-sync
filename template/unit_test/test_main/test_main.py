# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/3/28 10:32 下午

# desc:

import logging
import unittest
import main_frame.main as main


class TestMain(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestMain setUp:")

    def test_Main(self):
        main.Main(["-p", "1.prof"])

    def tearDown(self):
        logging.getLogger("myLog").debug("TestMain tearDown\n\n\n")


