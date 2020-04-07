# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/3 4:07 下午

import datetime
# desc:
import logging

import apscheduler.schedulers.background as background

import common.scheduler.datetime_data as datetime_data


class SchedulerMgr:
    def __init__(self):
        # xjctodo 需要每次从数据库初始化，取上次存的值，之后递增，作为notify的唯一ID
        self.m_nNotifyID = 0
        self.m_nNotifyInstID = 0

        self.m_dictNotify = {}

        self.m_JobMgr = None
        self.m_MailMgr = None

        self.m_dictJobCallback = {}

        self.m_LoggerObj = logging.getLogger("myLog")

    def Start(self):
        self.m_LoggerObj.info("Start")
        self.m_JobMgr = background.BackgroundScheduler()
        self.m_JobMgr.start()

        self._DailyUpdateNotifyIns()

    def Destroy(self):
        self.m_LoggerObj.info("Destroy")
        if self.m_JobMgr is not None:
            self.m_JobMgr.shutdown()

    def SetMailMgr(self, MailMgrObj):
        self.m_MailMgr = MailMgrObj

    # 日期，时间，提前多久提醒，提醒的内容（支持中英文）
    def RegisterNotify(self, szMsg,
                       DatetimeDataObj: datetime_data.DatetimeData,
                       nPreNotifySecond=0,
                       nCycleType=datetime_data.ECycleType.eOnce):

        import common.scheduler.base_notify as base_notify
        nNotifyID = self._GenNotifyID()
        self.m_dictNotify[nNotifyID] = base_notify.BaseNotify(szMsg,
                                                              DatetimeDataObj,
                                                              nPreNotifySecond,
                                                              nCycleType)

        return nNotifyID

    def UnRegisterNotify(self, nNotifyID):
        if nNotifyID in self.m_dictNotify:
            del self.m_dictNotify[nNotifyID]

    def ModifyNotify(self, nNotifyID, NotifyObj):
        if nNotifyID in self.m_dictNotify:
            self.m_dictNotify[nNotifyID] = NotifyObj

    def GetNotify(self, nNotifyID):
        return self.m_dictNotify[nNotifyID]

    def QueryNotify(self):
        return self.m_dictNotify

    def TryCreateNotifyInst(self, nNotifyID):
        if nNotifyID not in self.m_dictNotify:
            return False

        DatetimeObj = datetime.datetime.now()
        NotifyObj = self.m_dictNotify[nNotifyID]
        NotifyDatetimeObj = NotifyObj.GetNotifyDatetime(DatetimeObj)
        if NotifyDatetimeObj is None:
            return False

        self.AddTimeJob(self._NotifyMsg, NotifyDatetimeObj, nNotifyID, tupleArgs=(NotifyObj.Msg,))

        return True

    def AddTimeJob(self, CallbackObj, DatetimeObj, nNotifyID, tupleArgs=None):
        szJobID = self._GenJobID(nNotifyID)

        self.m_LoggerObj.info("Add job! time:%s, jobid:%s, args:%s", DatetimeObj.isoformat(), szJobID, str(tupleArgs))

        self._AddTimeJobCB(szJobID, CallbackObj, tupleArgs)

        self.m_JobMgr.add_job(self._OnTimeJobCB,
                              args=[szJobID],
                              trigger="date",
                              run_date=DatetimeObj,
                              id=szJobID)

    def _GenJobID(self, nNotifyID):
        return "%s_%s" % (nNotifyID, self._GenNotifyInstID())

    def _GenNotifyID(self):
        self.m_nNotifyID += 1
        return self.m_nNotifyID

    def _GenNotifyInstID(self):
        self.m_nNotifyInstID += 1
        return self.m_nNotifyInstID

    @staticmethod
    def _GetNextDayStart():
        DatetimeObj = datetime.datetime.now()
        TimedeltaObj = datetime.timedelta(days=1)
        StartOfToday = datetime.datetime(DatetimeObj.year, DatetimeObj.month, DatetimeObj.day)

        return StartOfToday + TimedeltaObj

    def _AddTimeJobCB(self, szJobID, CallbackObj, tupleArgs):
        assert szJobID not in self.m_dictJobCallback
        self.m_dictJobCallback[szJobID] = (CallbackObj, tupleArgs)

    def _RemoveTimeJobCB(self, szJobID):
        del self.m_dictJobCallback[szJobID]

    def _OnTimeJobCB(self, szJobID):
        assert szJobID in self.m_dictJobCallback

        CallbackObj, tupleArgs = self.m_dictJobCallback[szJobID]
        # self._RemoveTimeJob(szJobID)

        if tupleArgs is None:
            CallbackObj()
        else:
            CallbackObj(*tupleArgs)

    def _RemoveTimeJob(self, szJobID):
        self.m_LoggerObj.info("Remove job! jobid:%s", szJobID)
        self.m_JobMgr.remove_job(szJobID)

    def _NotifyMsg(self, szMsg):
        self.m_MailMgr.Send("jinchunxie@126.com", ["jinchunxie@126.com"], "小宝通知", szMsg)

    def _DailyUpdateNotifyIns(self, DatetimeObj=None):
        self.m_LoggerObj.info("Daily update notify ins")

        if DatetimeObj is None:
            DatetimeObj = datetime.datetime.now()

        self.AddTimeJob(self._DailyUpdateNotifyIns, self._GetNextDayStart(), 0)

        for nNotifyID, NotifyObj in self.m_dictNotify.items():
            NotifyDatetimeObj = NotifyObj.GetNotifyDatetime(DatetimeObj)
            if NotifyDatetimeObj is None:
                continue

            self.AddTimeJob(self._NotifyMsg, NotifyDatetimeObj, nNotifyID, tupleArgs=(NotifyObj.Msg,))
