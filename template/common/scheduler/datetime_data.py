# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/6 9:04 下午

# desc:weekday: Monday:0, Sunday:6

import re
import enum
import datetime
import borax.calendars.lunardate as lunardate

MINYEAR = 1
MAXYEAR = 9999
ONE_DAY_SECOND = 24 * 3600


def _CheckIntField(value):
    if isinstance(value, int):
        return value
    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value
            raise TypeError('__int__ returned non-int (type %s)' %
                            type(value).__name__)
        raise TypeError('an integer is required (got type %s)' %
                        type(value).__name__)
    raise TypeError('integer argument expected, got float')


@enum.unique
class ECycleType(enum.Enum):
    eOnce = 1  # 一次
    eDaily = 2  # 每天
    eWeekly = 3
    eMonthly = 4
    eYearly = 5


@enum.unique
class ECalendarType(enum.Enum):
    eSolar = 1  # 公历
    eLunar = 2  # 农历


class DateData:
    def __init__(self, nYear=2000, nMonth=1, nDay=1, nCalendarType=ECalendarType.eSolar):
        self._CheckDateFields(nYear, nMonth, nDay, nCalendarType)

        self.m_nYear = nYear
        self.m_nMonth = nMonth
        self.m_nDay = nDay
        self.m_nCalendarType = nCalendarType

    @classmethod
    def FromDateStr(cls, szDate, nCalendarType):
        MatchObj = re.match('^([0-9]+)-([0-9]+)-([0-9]+)$', szDate)
        if MatchObj is None:
            return False

        nYear = int(MatchObj.group(1))
        nMonth = int(MatchObj.group(2))
        nDay = int(MatchObj.group(3))

        return cls(nYear, nMonth, nDay, nCalendarType)

    @property
    def Year(self):
        return self.m_nYear

    @property
    def Month(self):
        return self.m_nMonth

    @property
    def Day(self):
        return self.m_nDay

    @property
    def CalendarType(self):
        return self.m_nCalendarType

    @staticmethod
    def _CheckDateFields(nYear, nMonth, nDay, nCalendarType):
        DateData._CheckYear(nYear)
        DateData._CheckMonth(nMonth)
        DateData._CheckDay(nDay)
        DateData._CheckCalendarType(nCalendarType)

    @staticmethod
    def _CheckYear(nYear):
        nYear = _CheckIntField(nYear)
        if not MINYEAR <= nYear <= MAXYEAR:
            raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), nYear)

    @staticmethod
    def _CheckMonth(nMonth):
        nMonth = _CheckIntField(nMonth)
        if not 1 <= nMonth <= 12:
            raise ValueError('month must be in 1..12', nMonth)

    @staticmethod
    def _CheckDay(nDay):
        nDay = _CheckIntField(nDay)
        if not 1 <= nDay <= 31:
            raise ValueError('day must be in 1..31', nDay)

    @staticmethod
    def _CheckCalendarType(nCalendarType):
        if nCalendarType not in ECalendarType:
            raise ValueError('calendar type not in ECalendarType')

    def Replace(self, nYear=None, nMonth=None, nDay=None):
        nYear = nYear if nYear is not None else self.m_nYear
        nMonth = nMonth if nMonth is not None else self.m_nMonth
        nDay = nDay if nDay is not None else self.m_nDay
        nCalendarType = self.m_nCalendarType

        return type(self)(nYear, nMonth, nDay, nCalendarType)

    def ToSolarDate(self) -> datetime.date:
        if self.CalendarType == ECalendarType.eLunar:
            LunarDateObj = lunardate.LunarDate(self.Year, self.Month, self.Day)
            return LunarDateObj.to_solar_date()
        else:
            return datetime.date(self.Year, self.Month, self.Day)

    def __eq__(self, OtherObj):
        if not isinstance(OtherObj, DateData):
            return False

        return self.Year == OtherObj.Year and self.Month == OtherObj.Month \
               and self.Day == OtherObj.Day and self.CalendarType == OtherObj.CalendarType


class TimeData:
    def __init__(self, nHour=0, nMinute=0, nSecond=0, nMicroSecond=0):
        self._CheckTimeFields(nHour, nMinute, nSecond, nMicroSecond)

        self.m_nHour = nHour
        self.m_nMinute = nMinute
        self.m_nSecond = nSecond
        self.m_nMicroSecond = nMicroSecond

    @classmethod
    def FromTimeStr(cls, szTime):
        MatchObj = re.match('^([0-9]+):([0-9]+):([0-9]+)$', szTime)
        if MatchObj is None:
            return False

        nHour = int(MatchObj.group(1))
        nMinute = int(MatchObj.group(2))
        nSecond = int(MatchObj.group(3))

        return cls(nHour, nMinute, nSecond)

    @property
    def Hour(self):
        return self.m_nHour

    @property
    def Minute(self):
        return self.m_nMinute

    @property
    def Second(self):
        return self.m_nSecond

    @property
    def MicroSecond(self):
        return self.m_nMicroSecond

    @staticmethod
    def _CheckTimeFields(nHour, nMinute, nSecond, nMicroSecond):
        nHour = _CheckIntField(nHour)
        nMinute = _CheckIntField(nMinute)
        nSecond = _CheckIntField(nSecond)
        nMicroSecond = _CheckIntField(nMicroSecond)
        if not 0 <= nHour <= 23:
            raise ValueError('hour must be in 0..23', nHour)
        if not 0 <= nMinute <= 59:
            raise ValueError('minute must be in 0..59', nMinute)
        if not 0 <= nSecond <= 59:
            raise ValueError('second must be in 0..59', nSecond)
        if not 0 <= nMicroSecond <= 999999:
            raise ValueError('microsecond must be in 0..999999', nMicroSecond)

    def Replace(self, nHour=None, nMinute=None, nSecond=None, nMicroSecond=None):
        nHour = nHour if nHour is not None else self.m_nHour
        nMinute = nMinute if nMinute is not None else self.m_nMinute
        nSecond = nSecond if nSecond is not None else self.m_nSecond
        nMicroSecond = nMicroSecond if nMicroSecond is not None else self.m_nMicroSecond

        return type(self)(nHour, nMinute, nSecond, nMicroSecond)

    def __eq__(self, OtherObj) -> bool:
        if not isinstance(OtherObj, TimeData):
            return False

        return self.Hour == OtherObj.Hour and self.Minute == OtherObj.Minute \
               and self.Second == OtherObj.Second and self.MicroSecond == OtherObj.MicroSecond


class DatetimeData:
    def __init__(self, nYear=2000, nMonth=1, nDay=1, nHour=0, nMinute=0, nSecond=0, nMicroSecond=0, nWeekday=0,
                 nCalendarType=ECalendarType.eSolar):
        self._CheckWeekDay(nWeekday)

        self.m_DateDataObj = DateData(nYear=nYear, nMonth=nMonth, nDay=nDay, nCalendarType=nCalendarType)
        self.m_TimeDataObj = TimeData(nHour=nHour, nMinute=nMinute, nSecond=nSecond, nMicroSecond=nMicroSecond)

        self.m_nWeekday = nWeekday

    @classmethod
    def FromDateDataTimeData(cls, DateDataObj, TimeDataObj, nWeekday):
        return cls(DateDataObj.Year, DateDataObj.Month, DateDataObj.Day,
                   TimeDataObj.Hour, TimeDataObj.Minute, TimeDataObj.Second, TimeDataObj.MicroSecond,
                   nWeekday=nWeekday, nCalendarType=DateDataObj.CalendarType)

    @property
    def Year(self):
        return self.m_DateDataObj.Year

    @property
    def Month(self):
        return self.m_DateDataObj.Month

    @property
    def Day(self):
        return self.m_DateDataObj.Day

    @property
    def CalendarType(self):
        return self.m_DateDataObj.CalendarType

    @property
    def Hour(self):
        return self.m_TimeDataObj.Hour

    @property
    def Minute(self):
        return self.m_TimeDataObj.Minute

    @property
    def Second(self):
        return self.m_TimeDataObj.Second

    @property
    def MicroSecond(self):
        return self.m_TimeDataObj.MicroSecond

    @property
    def Weekday(self):
        return self.m_nWeekday

    @classmethod
    def FromDatetime(cls, DatetimeObj, nCalenderType=ECalendarType.eSolar):
        nYear, nMonth, nDay = DatetimeObj.year, DatetimeObj.month, DatetimeObj.day
        if nCalenderType == ECalendarType.eLunar:
            LunarDateObj = lunardate.LunarDate.from_solar_date(nYear, nMonth, nDay)
            nYear, nMonth, nDay = LunarDateObj.year, LunarDateObj.month, LunarDateObj.day

        nHour, nMinute, nSecond = DatetimeObj.hour, DatetimeObj.minute, DatetimeObj.second
        nMicroSecond = DatetimeObj.microsecond
        nWeekday = DatetimeObj.weekday()
        return cls(nYear, nMonth, nDay, nHour, nMinute, nSecond, nMicroSecond, nWeekday, nCalenderType)

    def ToDatetime(self):
        if self.CalendarType == ECalendarType.eSolar:
            return datetime.datetime(self.Year, self.Month, self.Day, self.Hour, self.Minute, self.Second,
                                     self.MicroSecond)
        else:
            SolarDateObj = self.m_DateDataObj.ToSolarDate()
            return datetime.datetime(SolarDateObj.year, SolarDateObj.month, SolarDateObj.day, self.Hour, self.Minute,
                                     self.Second, self.MicroSecond)

    @property
    def DateData(self) -> DateData:
        return self.m_DateDataObj

    @property
    def TimeData(self) -> TimeData:
        return self.m_TimeDataObj

    def Replace(self, nYear=None, nMonth=None, nDay=None, nHour=None, nMinute=None, nSecond=None, nMicroSecond=None,
                nWeekday=None):
        DateDataObj = self.m_DateDataObj.Replace(nYear, nMonth, nDay)
        TimeDataObj = self.m_TimeDataObj.Replace(nHour, nMinute, nSecond, nMicroSecond)
        nWeekday = nWeekday if nWeekday is not None else self.Weekday

        return type(self)(DateDataObj.Year, DateDataObj.Month, DateDataObj.Day, TimeDataObj.Hour, TimeDataObj.Minute,
                          TimeDataObj.Second, TimeDataObj.MicroSecond, nWeekday, DateDataObj.CalendarType)

    def __eq__(self, OtherObj):
        return self.DateData == OtherObj.DateData and self.TimeData == OtherObj.TimeData and \
               self.Weekday == OtherObj.Weekday

    @staticmethod
    def _CheckWeekDay(nWeekday):
        """weekday: Monday:0, Sunday:6"""
        if not 0 <= nWeekday <= 23:
            raise ValueError('weekday must be in 0..6', nWeekday)
