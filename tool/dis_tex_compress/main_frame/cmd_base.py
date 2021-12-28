# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/11/11 8:10

# desc:
# 所有命令类的基类
# 1、在main_frame/command下新增cmd开头的py文件
# 2、希望实现新的类型时，需要继承与CmdBase，然后，实现GetName，Init，Do等函数
# 3、在启动中传入命令名和命令需要的参数

# 以配置表转表工具为例
# 1、在main_frame/command下新增文件cmd_excel2py.py
# 2、新类型的代码：main_frame.command.cmd_excel2py.py，其中CmdExcel2Py是我们实现的命令类，其继承与CmdBase，实现了GetName，Init，Do等函数
# 3、启动脚本如下，其中excel2py是命令名，即GetName返回的名字，后面两个是在命令类中需要用到的参数
#   python main_frame/main.py excel2py config/excel config/setting

import common.my_log as my_log


class CmdBase:
    def __init__(self):
        self.m_AppObj = None
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "base_command"

    def Init(self, AppObj):
        """初始化AppObj"""
        self.m_LoggerObj.debug("Init cmd: %s", self.GetName())

        self.m_AppObj = AppObj
        self._OnInit()

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start DoExcel2Py")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        # 可以通过self.m_AppObj.CLM获得参数
        # szExcelPath = self.m_AppObj.CLM.GetArg(1)
        # szSettingPath = self.m_AppObj.CLM.GetArg(2)
