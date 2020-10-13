# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/10/13 20:52:37

# desc: desc


import logging
import unittest

import common.notify.ding_ding_mgr as ding_ding_mgr


class TestDingDingMgr(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestDingDingMgr setUp:")

        self.m_DingDingMgrObj = ding_ding_mgr.DingDingMgr(
            ding_ding_mgr.g_szWebhook, ding_ding_mgr.g_szSecret, ding_ding_mgr.g_szKeyWord, ["手机号"])

    def test_Send(self):
        # self.m_DingDingMgrObj.Send("hello, xiaobao")
        self.assertEqual(1, 1)

    def tearDown(self):
        logging.getLogger("myLog").debug("TestDingDingMgr tearDown\n\n\n")
