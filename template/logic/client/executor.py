import time


class Executor:
    """"""

    def __init__(self, dictData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szListenIp = dictData["listen_ip"]
        self.m_nListenPort = dictData["listen_port"]
        self.m_szRegisterIp = dictData["register_ip"]
        self.m_nRegisterPort = dictData["register_port"]

    @property
    def ListenIp(self):
        return self.m_szRegisterIp

    @property
    def ListenPort(self):
        return self.m_nListenPort

    def Run(self):
        self.m_LoggerObj.info("")

        self._OnStart()

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        while True:
            time.sleep(0.01)
            xx_connection_mgr.Update()

    # ********************************************************************************
    # private
    # ********************************************************************************
    def _OnStart(self):
        self.m_LoggerObj.debug("")

        self._StartListen()
        self._StartRegister()

    def _StartListen(self):
        self.m_LoggerObj.debug("")

        import common.async_net as async_net
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData(nSocketListen=10)

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eServer,
            dictConnectionData
        )

        try:
            async_net.xx_connection_mgr.Listen(nConnectionID, self.m_szListenIp, self.m_nListenPort)
        except Exception as e:
            raise e

    def _StartRegister(self):
        self.m_LoggerObj.debug("")

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData(ExecutorObj=self,
                                                                    nAutoReconnectMaxCount=10,
                                                                    nAutoReconnectInterval=10)

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eExecutor,
            dictConnectionData)

        xx_connection_mgr.Connect(nConnectionID, self.m_szRegisterIp, self.m_nRegisterPort)
