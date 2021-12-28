# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

import time


class RegisterServer:
    """"""

    def __init__(self, dictData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szListenIp = dictData["listen_ip"]
        self.m_nListenPort = dictData["listen_port"]

    def Run(self):
        self.m_LoggerObj.info("Run register server")

        self._OnStart()

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import logic.task.assign_task_mgr as assign_task_mgr
        while True:
            time.sleep(0.01)
            xx_connection_mgr.Update()
            assign_task_mgr.Update()


    # ********************************************************************************
    # private
    # ********************************************************************************
    def _OnStart(self):
        self.m_LoggerObj.debug("")

        self._StartListen()

    def _StartListen(self):
        self.m_LoggerObj.debug("")

        import common.async_net as async_net
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData(nSocketListen=10)

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eReg,
            dictConnectionData
        )

        try:
            async_net.xx_connection_mgr.Listen(nConnectionID, self.m_szListenIp, self.m_nListenPort)
        except Exception as e:
            raise e
