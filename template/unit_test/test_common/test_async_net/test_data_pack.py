# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/13 14:17

# desc: 用于测试data pack


__all__ = []

# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


# if __name__ == '__main__':
#     unittest.main()


import logging
import unittest

import common.async_net.pack.data_pack as data_pack


class TestDataPack(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestDataPack setUp:")

    # def test_fun(self):
    # main.Main(["main_frame/main.py", "excel2py", "config/excel", "config/setting"])
    def test_pack_unpack(self):
        dictData = {"name": "xjc", "age": 16, "ismale": True}
        byteData = data_pack.Serialize(dictData)
        dictUnpackData = data_pack.Unserialize(byteData)

    def tearDown(self):
        logging.getLogger("myLog").debug("TestAAA tearDown\n\n\n")
