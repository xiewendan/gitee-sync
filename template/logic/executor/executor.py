# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:05

# desc:

import time
import uuid


class Executor:
    """"""

    def __init__(self, dictData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szListenIp = dictData["listen_ip"]
        self.m_nListenPort = dictData["listen_port"]
        self.m_szRegisterIp = dictData["register_ip"]
        self.m_nRegisterPort = dictData["register_port"]
        self.m_szFileListenIp = dictData["file_listen_ip"]
        self.m_nFileListenPort = dictData["file_listen_port"]
        self.m_nRegisterConnID = 0

        self.m_szExeUuid = uuid.uuid1()

    @property
    def ListenIp(self):
        return self.m_szRegisterIp

    @property
    def ListenPort(self):
        return self.m_nListenPort

    def Run(self):
        self.m_LoggerObj.info("")

        self._OnStart()

        import logic.task.dis_task_mgr as dis_task_mgr
        import logic.task.accept_task_mgr as accept_task_mgr


        dis_task_mgr.SetIpPort(self.m_szListenIp, self.m_nListenPort, self.m_nFileListenPort)
        nRegisterConnID = self._GetRegisterConnID()
        dis_task_mgr.SetRegisterConnID(nRegisterConnID)

        import common.xx_time as xx_time
        nCurTime = xx_time.GetTime()

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        while True:
            time.sleep(0.01)
            xx_connection_mgr.Update()
            dis_task_mgr.Update(nCurTime)
            accept_task_mgr.Update(nCurTime)


    # ********************************************************************************
    # private
    # ********************************************************************************
    def _OnStart(self):
        self.m_LoggerObj.debug("")

        import common.async_net.connection.xx_connection as xx_connection

        self._StartListen(xx_connection.EConnectionType.eExe, self.m_szListenIp, self.m_nListenPort)
        self._StartListen(xx_connection.EConnectionType.eFileExe, self.m_szFileListenIp, self.m_nFileListenPort)

        self._StartRegister()

    def _StartListen(self, nConnectionType, szIp, nPort, nListenCount=10):
        self.m_LoggerObj.debug("ConnectionType:%d, ip:%s, port:%d, listenCount:%d", nConnectionType, szIp, nPort, nListenCount)

        import common.async_net as async_net
        import common.async_net.xx_connection_mgr as xx_connection_mgr

        dictConnectionData = xx_connection_mgr.CreateConnectionData(nSocketListen=nListenCount)
        nConnectionID = xx_connection_mgr.CreateConnection(nConnectionType, dictConnectionData)

        try:
            async_net.xx_connection_mgr.Listen(nConnectionID, szIp, nPort)
        except Exception as e:
            raise e

    def _StartRegister(self):
        self.m_LoggerObj.debug("")

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData(ExecutorObj=self, nAutoReconnectMaxCount=10, nAutoReconnectInterval=10)

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eExe2Reg,
            dictConnectionData)

        xx_connection_mgr.Connect(nConnectionID, self.m_szRegisterIp, self.m_nRegisterPort)
        self.m_nRegisterConnID = nConnectionID

    def _GetRegisterConnID(self):
        assert self.m_nRegisterConnID != 0
        return self.m_nRegisterConnID
