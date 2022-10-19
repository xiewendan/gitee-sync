# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/9 9:53 上午

# desc:
import common.scheduler.datetime_data as datetime_data


class NotifyConfig:
    def __init__(self, NotifyData):
        self._CheckData(NotifyData)

        self.m_nNotifyID = NotifyData["id"]

        nCalendarType = self._GetCalendarType(NotifyData["calendar_type"])
        DateDataObj = datetime_data.DateData.FromDateStr(NotifyData["date"], nCalendarType)
        TimeDataObj = datetime_data.TimeData.FromTimeStr(NotifyData["time"])
        nWeekday = NotifyData["weekday"]
        self.m_DatetimeDataObj = datetime_data.DatetimeData.FromDateDataTimeData(DateDataObj, TimeDataObj, nWeekday)

        self.m_nPreNotifySecond = NotifyData["pre_notify"]
        self.m_nCycleType = self._GetCycleType(NotifyData["cycle_type"])
        self.m_szMsg = NotifyData["msg"]

    @staticmethod
    def _CheckData(NotifyData):
        assert isinstance(NotifyData["id"], int) and NotifyData["id"] > 0, "输入id必须是大于0的整数"
        assert isinstance(NotifyData["msg"], str) and NotifyData["msg"] != "", "输入msg不应为空"
        assert NotifyData["calendar_type"] in ("lunar", "solar"), "calendar type 必须是 lunar或solar"
        assert NotifyData["pre_notify"] >= 0, "提前通知的时间必须大于等于0"
        assert 0 <= NotifyData["weekday"] <= 6, "weekday必须是大于等于0小于等于6"

    @staticmethod
    def _GetCalendarType(szCalendarType):
        if szCalendarType == "lunar":
            return datetime_data.ECalendarType.eLunar
        elif szCalendarType == "solar":
            return datetime_data.ECalendarType.eSolar
        else:
            assert False

    @staticmethod
    def _GetCycleType(szCycleType):
        dictCycle = {
            "once": datetime_data.ECycleType.eOnce,
            "daily": datetime_data.ECycleType.eDaily,
            "weekly": datetime_data.ECycleType.eWeekly,
            "monthly": datetime_data.ECycleType.eMonthly,
            "yearly": datetime_data.ECycleType.eYearly
        }

        assert szCycleType in dictCycle, \
            "Error value: {0}, 循环值范围是：once, daily, weekly, monthly, yearly".format(szCycleType, )
        return dictCycle[szCycleType]

    @property
    def NotifyID(self):
        return self.m_nNotifyID

    @property
    def DatetimeData(self):
        return self.m_DatetimeDataObj

    @property
    def PreNotifySecond(self):
        return self.m_nPreNotifySecond

    @property
    def CycleType(self):
        return self.m_nCycleType

    @property
    def Msg(self):
        return self.m_szMsg
