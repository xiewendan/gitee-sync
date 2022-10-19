# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/25 19:59

# desc: cmd的template模板


import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdTemplate(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "template"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
