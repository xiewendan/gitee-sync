# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 19:10

# desc: 邮件服务

import common.my_log as my_log

import common.notify.mail_mgr as mail_mgr
import main_frame.service_base as service_base


class MailService(service_base.ServiceBase):
    def __init__(self):
        super().__init__()
        self.m_MailMgr = None
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetOptList():
        return ["-m", "--mail"]

    @staticmethod
    def GetName():
        return "mail"

    def _OnInit(self):
        self.m_LoggerObj.debug("_OnInit")
        self._InitMailMgr()

    def _OnDestroy(self):
        self.m_LoggerObj.debug("_OnDestroy")
        self._DestroyMailMgr()

    def GetMailMgr(self):
        assert self.m_MailMgr is not None
        return self.m_MailMgr

    def _InitMailMgr(self):
        self.m_LoggerObj.info("Init mail mgr")

        self.m_MailMgr = mail_mgr.MailMgr()

        self.m_MailMgr.SetDefaultConfig(
            self.GetApp().ConfigLoader.MailHost,
            self.GetApp().ConfigLoader.MailUser,
            self.GetApp().ConfigLoader.MailPassword,
            self.GetApp().ConfigLoader.MailTo)

        self.m_MailMgr.Send("启动小小服务", "你好，我是小小助手，我已经启动了，你可以直接找我哈")

        self.m_LoggerObj.info("Init mail mgr end\n")

    def _DestroyMailMgr(self):
        self.m_LoggerObj.debug("_DestroyMailMgr")

        if self.m_MailMgr is not None:
            self.m_LoggerObj.debug("destroy mail mgr")
            self.m_MailMgr.Destroy()
            self.m_MailMgr = None
