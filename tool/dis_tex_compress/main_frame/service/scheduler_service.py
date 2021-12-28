# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/2 20:58

# desc: 通知系统

import common.my_log as my_log
import common.scheduler.scheduler_mgr as scheduler_mgr
import main_frame.service_base as service_base


class SchedulerService(service_base.ServiceBase):
    def __init__(self):
        super().__init__()
        self.m_SchedulerMgr = None
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetOptList():
        return ["-s", "--scheduler"]

    @staticmethod
    def GetName():
        return "scheduler"

    def GetSchedulerMgr(self):
        return self.m_SchedulerMgr

    def _GetDepServiceList(self):
        return ["ding_ding", "mail"]

    def _OnInit(self):
        self.m_LoggerObj.debug("_OnInit")
        self._InitSchedulerMgr()

    def _OnDestroy(self):
        self.m_LoggerObj.debug("_OnDestroy")
        self._DestroySchedulerMgr()

    def _DestroySchedulerMgr(self):
        self.m_LoggerObj.debug("_DestroySchedulerMgr")

        if self.m_SchedulerMgr is not None:
            self.m_LoggerObj.debug("destroy scheduler mgr")
            self.m_SchedulerMgr.Destroy()
            self.m_SchedulerMgr = None

    def _InitSchedulerMgr(self):
        self.m_LoggerObj.info("Init scheduler mgr")

        MailMgrObj = self.GetApp().GetService("mail").GetMailMgr()
        assert MailMgrObj is not None, "scheduler mgr depend on mail mgr"

        DingDingMgrObj = self.GetApp().GetService("ding_ding").GetDingDingMgr()
        assert DingDingMgrObj is not None, "scheduler mgr depend on ding ding mgr"

        self.m_SchedulerMgr = scheduler_mgr.SchedulerMgr()
        self.m_SchedulerMgr.SetMailMgr(MailMgrObj)
        self.m_SchedulerMgr.SetDingDingMgr(DingDingMgrObj)

        self.m_SchedulerMgr.Init()
        self.m_SchedulerMgr.Start()

        self.m_LoggerObj.info("Init scheduler mgr end\n")
