# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/13 14:17

# desc: 用于测试data pack


import logging
import unittest

import common.async_net.pack.data_pack as data_pack
import unit_test.unit_test_helper as unit_test_helper


class TestDataPack(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestDataPack setUp:")

    def test_pack_unpack(self):
        dictData = {"name": "xjc", "age": 16, "ismale": True}
        byteData = data_pack.Serialize(dictData)
        dictUnpackData = data_pack.Unserialize(byteData)

        self.assertTrue(unit_test_helper.CompareDict(dictData, dictUnpackData))

    def tearDown(self):
        logging.getLogger("myLog").debug("TestDataPack tearDown\n\n\n")
