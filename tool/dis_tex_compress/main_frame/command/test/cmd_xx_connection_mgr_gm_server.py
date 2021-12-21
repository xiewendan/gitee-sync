# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:


import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdXxConnectionMgrGmServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "xx_connection_mgr_gm_server"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        # szCWD = self.m_AppObj.ConfigLoader.CWD

        szIp = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))
        # szTargetIp = self.m_AppObj.CLM.GetArg(3)
        # nTargetPort = int(self.m_AppObj.CLM.GetArg(4))

        import common.async_net as async_net
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData(nSocketListen=10)

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eServer,
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

        # xx_connection_mgr.Destroy()
