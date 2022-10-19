# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 20:50

# desc: dingding服务，用于发送消息

import common.my_log as my_log
import main_frame.service_base as service_base
import common.notify.ding_ding_mgr as ding_ding_mgr


class DingDingService(service_base.ServiceBase):
    def __init__(self):
        super().__init__()
        self.m_DingDingMgr = None
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetOptList():
        return ["-d", "--dingding"]

    @staticmethod
    def GetName():
        return "ding_ding"

    def _OnInit(self):
        self.m_LoggerObj.debug("_OnInit")
        self._InitDingDingMgr()

    def _OnDestroy(self):
        self.m_LoggerObj.debug("_OnDestroy")
        self._DestroyDingDingMgr()

    def GetDingDingMgr(self):
        assert self.m_DingDingMgr is not None
        return self.m_DingDingMgr

    def _InitDingDingMgr(self):
        self.m_LoggerObj.info("Start dingding mgr")

        self.m_DingDingMgr = ding_ding_mgr.DingDingMgr(
            self.GetApp().ConfigLoader.DingDingWebhook,
            self.GetApp().ConfigLoader.DingDingSecret,
            self.GetApp().ConfigLoader.DingDingKeyword,
            [self.GetApp().ConfigLoader.DingDingTo]
        )

        self.m_DingDingMgr.Send(
            "你好，我是小小助手，我已经启动了，你可以直接找我哈"
        )

        self.m_LoggerObj.info("End dingding mgr\n")

    def _DestroyDingDingMgr(self):
        self.m_LoggerObj.debug("_DestroyDingDingMgr")

        if self.m_DingDingMgr is not None:
            self.m_LoggerObj.debug("destroy ding ding mgr")

            self.m_DingDingMgr.Destroy()
            self.m_DingDingMgr = None
