# -*- coding: utf-8 -*-
# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:


import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdRegisterServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "register_server"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start cmd: %s", self.GetName())

        # szCWD = self.m_AppObj.ConfigLoader.CWD

        dictData = {
            "listen_ip": "0.0.0.0",
            "listen_port": 50000
        }

        import logic.register.register_server as register_server
        RegisterServerObj = register_server.RegisterServer(dictData)
        RegisterServerObj.Run()
