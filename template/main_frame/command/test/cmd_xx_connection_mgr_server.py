# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:

import socket

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdXxConnectionMgrServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "xx_connection_mgr_server"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        szTargetIp = self.m_AppObj.CLM.GetArg(3)
        nTargetPort = int(self.m_AppObj.CLM.GetArg(4))

        import common.async_net as async_net

        dictConnectionData = async_net.xx_connection_mgr.CreateConnectionData(nSocketFamily=socket.AF_INET,
                                                                              nSocketType=socket.SOCK_STREAM)

        nConnectionID = async_net.xx_connection_mgr.CreateConnection(
            async_net.connection.xx_connection.EConnectionType.eServer,
            dictConnectionData
        )
        try:
            async_net.xx_connection_mgr.Listen(nConnectionID, szIp, nPort)
        except Exception as e:
            raise e

        import time

        while True:
            time.sleep(1)
            async_net.xx_connection_mgr.Update()

        # async_net.xx_connection_mgr.Destroy()
