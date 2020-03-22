# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 3:26 PM

# desc:

import main_frame.base_app as base_app


def GetAppCls():
    return MainApp


class MainApp(base_app.BaseApp):
    @staticmethod
    def GetConfigLoaderCls():
        import logic.my_config_loader as my_config_loader
        return my_config_loader.MyConfigLoader

    def OnLogic(self):
        print("xjc")
        pass
