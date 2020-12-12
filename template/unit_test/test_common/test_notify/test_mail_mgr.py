# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 14:14

# desc: 支持mul thread


import logging
import unittest

import main_frame.main as main
import common.notify.mail_mgr as mail_mgr
import threading


class TestMailMgr(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestMailMgr setUp:")

        self.m_MailMgrObj = mail_mgr.MailMgr()
        self.m_MailMgrObj.SetDefaultConfig(g_TestAppObj.ConfigLoader.MailHost, g_TestAppObj.ConfigLoader.MailUser,
                                           g_TestAppObj.ConfigLoader.MailPassword, g_TestAppObj.ConfigLoader.MailTo)
        self.m_MailMgrObj.UnLogin()

    def SendMsg(self, nIndex):
        self.m_MailMgrObj.Send("小宝通知", "专注，技术，管理 {}".format(nIndex))

    # 多线程测试send接口
    def test_send(self):
        listThreads = []
        for nIndex in range(3):
            logging.getLogger("myLog").debug("create and start thread %d", nIndex)
            ThreadObj = threading.Thread(target=self.SendMsg, args=(nIndex,))
            listThreads.append(ThreadObj)
            ThreadObj.start()

        for nIndex, ThreadObj in enumerate(listThreads):
            logging.getLogger("myLog").debug("before joining thread %d", nIndex)
            ThreadObj.join()
            logging.getLogger("myLog").debug("before joining thread %d", nIndex)

        # main.Main(["main_frame/main.py", "excel2py", "config/excel", "config/setting"])

    def tearDown(self):
        self.m_MailMgrObj.Destroy()
        logging.getLogger("myLog").debug("TestMailMgr tearDown\n\n\n")
