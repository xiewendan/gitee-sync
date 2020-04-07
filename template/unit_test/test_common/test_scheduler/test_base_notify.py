# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/6 10:44 下午

# desc: 


import logging
import unittest
import datetime
import common.scheduler.base_notify as base_notify
import common.scheduler.datetime_data as datetime_data


class TestBaseNotify(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestBaseNotify setUp:")

    def test_GetNotifyDatetime(self):
        # 1 字符串
        DatetimeDataObj = datetime_data.DatetimeData()
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eOnce)
        self.assertEqual(BaseNotifyObj.Msg, "", "字符串错误")
        BaseNotifyObj = base_notify.BaseNotify("xjc", DatetimeDataObj, 0, datetime_data.ECycleType.eOnce)
        self.assertEqual(BaseNotifyObj.Msg, "xjc", "字符串错误")

        # 2 指定日期
        # * 2.1 公历
        DatetimeDataObj = datetime_data.DatetimeData(2000, 1, 1, 0, 0, 0, 0)
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eOnce)
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(1999, 12, 31, 23, 59, 59, 0)), "公历日期前一天不提醒")
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 1, 12, 0, 0, 0)),
                         DatetimeDataObj.ToDatetime(), "公历日期当天有提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)), "公历日期后一天不提醒")

        # * 2.2 农历
        DatetimeDataObj = datetime_data.DatetimeData(1999, 11, 25, 0, 0, 0, 0, nCalendarType=datetime_data.ECalendarType.eLunar)
        print(DatetimeDataObj.ToDatetime())
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eOnce)
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(1999, 12, 31, 23, 59, 59, 0)), "农历日期前一天有提醒")
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 1, 12, 0, 0, 0)),
                         DatetimeDataObj.ToDatetime(), "农历日期当天没有提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)), "农历日期后一天有提醒")

        # 3 提前通知
        # * 一天
        DatetimeDataObj = datetime_data.DatetimeData(2000, 1, 1, 0, 0, 0, 0)
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 24 * 3600, datetime_data.ECycleType.eOnce)
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(1999, 12, 31, 23, 59, 59, 0)),
                         DatetimeDataObj.ToDatetime() - datetime.timedelta(days=1), "公历日期提前一天应该提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 1, 12, 0, 0, 0)),
                          "公历日历提前一天提醒，在当天不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)),
                          "公历日历提前一天提醒，在后一天不提醒")

        # 4 循环类型
        # * 4.1 周
        DatetimeObj = datetime.datetime(2000, 1, 1, 12, 0, 0, 0)  # 周六
        DatetimeDataObj = datetime_data.DatetimeData.FromDatetime(DatetimeObj)
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eWeekly)

        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(DatetimeObj), DatetimeObj, "周六正常提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)), "周日不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 3, 0, 0, 0, 0)), "周一不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 4, 0, 0, 0, 0)), "周二不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 5, 0, 0, 0, 0)), "周三不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 6, 0, 0, 0, 0)), "周四不提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 7, 0, 0, 0, 0)), "周五不提醒")
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 8, 0, 0, 0, 0)),
                         datetime.datetime(2000, 1, 8, 12, 0, 0, 0), "周六提醒")
        # * 4.2 年
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eYearly)
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2001, 1, 1, 0, 0, 0, 0)),
                         datetime.datetime(2001, 1, 1, 12, 0, 0, 0), "每年1月1号提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)), "非1月1号不提醒")

        # * 4.2 月
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eMonthly)
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2001, 2, 1, 0, 0, 0, 0)),
                         datetime.datetime(2001, 2, 1, 12, 0, 0, 0), "每月1号提醒")
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2001, 3, 1, 0, 0, 0, 0)),
                         datetime.datetime(2001, 3, 1, 12, 0, 0, 0), "每月1号提醒")
        self.assertIsNone(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2000, 1, 2, 0, 0, 0, 0)), "非每月1号不提醒")

        # * 4.2 日
        BaseNotifyObj = base_notify.BaseNotify("", DatetimeDataObj, 0, datetime_data.ECycleType.eDaily)
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2001, 2, 2, 0, 0, 0, 0)),
                         datetime.datetime(2001, 2, 2, 12, 0, 0, 0), "每天提醒")
        self.assertEqual(BaseNotifyObj.GetNotifyDatetime(datetime.datetime(2001, 3, 4, 0, 0, 0, 0)),
                         datetime.datetime(2001, 3, 4, 12, 0, 0, 0), "每天提醒")

        pass

    def tearDown(self):
        logging.getLogger("myLog").debug("TestBaseNotify tearDown\n\n\n")
