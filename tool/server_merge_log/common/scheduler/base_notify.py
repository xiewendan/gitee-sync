# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/3 10:21 下午

# desc:

import datetime
import common.scheduler.datetime_data as datetime_data


class BaseNotify:
    def __init__(self, szMsg: str, DatetimeDateObj: datetime_data.DatetimeData, nPreNotifySecond: int,
                 nCycleType: datetime_data.ECycleType):
        assert nPreNotifySecond >= 0

        self.m_szMsg = szMsg
        self.m_datetimeDataObj = DatetimeDateObj
        self.m_nPreNotifySecond = nPreNotifySecond
        self.m_nCycleType = nCycleType

    def GetNotifyDatetime(self, CurDatetimeObj: datetime.datetime) -> datetime:
        CurDatetimeObj = CurDatetimeObj + datetime.timedelta(seconds=self.m_nPreNotifySecond)
        CurDatetimeDataObj = datetime_data.DatetimeData.FromDatetime(CurDatetimeObj,
                                                                     self.m_datetimeDataObj.CalendarType)
        RetDatetimeDataObj = None

        if self.m_nCycleType == datetime_data.ECycleType.eOnce:
            if self.m_datetimeDataObj.DateData == CurDatetimeDataObj.DateData:
                RetDatetimeDataObj = self.m_datetimeDataObj

        elif self.m_nCycleType == datetime_data.ECycleType.eDaily:
            nYear, nMonth, nDay = CurDatetimeDataObj.Year, CurDatetimeDataObj.Month, CurDatetimeDataObj.Day
            RetDatetimeDataObj = self.m_datetimeDataObj.Replace(nYear=nYear, nMonth=nMonth, nDay=nDay)

        elif self.m_nCycleType == datetime_data.ECycleType.eMonthly:
            if self.m_datetimeDataObj.Day == CurDatetimeDataObj.Day:
                nYear = CurDatetimeDataObj.Year
                nMonth = CurDatetimeDataObj.Month
                RetDatetimeDataObj = self.m_datetimeDataObj.Replace(nYear=nYear, nMonth=nMonth)

        elif self.m_nCycleType == datetime_data.ECycleType.eYearly:
            if self.m_datetimeDataObj.Month == CurDatetimeDataObj.Month and \
                    self.m_datetimeDataObj.Day == CurDatetimeDataObj.Day:
                nYear = CurDatetimeDataObj.Year
                RetDatetimeDataObj = self.m_datetimeDataObj.Replace(nYear=nYear)

        elif self.m_nCycleType == datetime_data.ECycleType.eWeekly:
            if self.m_datetimeDataObj.Weekday == CurDatetimeDataObj.Weekday:
                nYear, nMonth, nDay = CurDatetimeDataObj.Year, CurDatetimeDataObj.Month, CurDatetimeDataObj.Day
                RetDatetimeDataObj = self.m_datetimeDataObj.Replace(nYear=nYear, nMonth=nMonth, nDay=nDay)

        else:
            assert False, "undefine CycleType %s" % str(self.m_nCycleType)

        if RetDatetimeDataObj is None:
            return None
        else:
            RetDatetimeObj = RetDatetimeDataObj.ToDatetime()
            RetDatetimeObj = RetDatetimeObj - datetime.timedelta(seconds=self.m_nPreNotifySecond)

            return RetDatetimeObj

    @property
    def Msg(self):
        return self.m_szMsg
