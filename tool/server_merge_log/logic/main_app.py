# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 3:26 PM

# desc:


import time
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
        if not self.IsTest():
            self.MainLoop()

    def MainLoop(self):
        try:
            time.sleep(1)
            self.m_LoggerObj.info("main loop")
        except (KeyboardInterrupt, SystemExit):
            self.Destroy()

