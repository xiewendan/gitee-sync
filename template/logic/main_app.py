# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 3:26 PM

# desc:

import time

import common.scheduler.datetime_data as datetime_data
import main_frame.base_app as base_app


def GetAppCls():
    return MainApp


class MainApp(base_app.BaseApp):
    @staticmethod
    def GetCommandOpt():
        return "", []

    @staticmethod
    def GetConfigLoaderCls():
        import logic.my_config_loader as my_config_loader
        return my_config_loader.MyConfigLoader

    def GetLeftDay(self):
        pass

    def OnLogic(self):
        szMsg = "蛋仔生日:2020,3月18号"
        nCalendar = datetime_data.ECalendarType.eLunar
        DatetimeDataObj = datetime_data.DatetimeData(2020, 3, 18, 12, 0, 0, 0, nCalendarType=nCalendar)
        self.GetSchedulerMgr().RegisterNotify(szMsg,
                                              DatetimeDataObj,
                                              nPreNotifySecond=2 * datetime_data.ONE_DAY_SECOND,
                                              nCycleType=datetime_data.ECycleType.eYearly)

        self.MainLoop()

    def MainLoop(self):
        try:
            # 其他任务是独立的线程执行
            while True:
                time.sleep(5)
                self.Info("main loop")
        except (KeyboardInterrupt, SystemExit):
            self.Destroy()
