# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/08/08 12:47:48

# desc: desc

import unittest
import logging
import common.my_path as my_path

class TestMyPath(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestMyPath setUp:")

    def test_FileExt(self):
        self.assertEqual(my_path.FileExt("c:/123/xjc.txt"), ".txt")
        self.assertEqual(my_path.FileExt("c:/123/xjc.txt"), ".jpg")
    
    def tearDown(self):
        logging.getLogger("myLog").debug("TestMyPath tearDown")
        