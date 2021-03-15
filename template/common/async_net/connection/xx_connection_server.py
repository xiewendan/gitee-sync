import common.async_net.connection.xx_connection as xx_connection
import common.async_net.connection.xx_connection_base as xx_connection_base


class XxConnectionServer(xx_connection_base.XxConnectionBase):
    """"""

    def __init__(self, dictConnectionData):
        super().__init__(dictConnectionData)

        self.m_nListenCount = dictConnectionData["socket_listen"]

        self.m_eConnectState = xx_connection.EConnectionState.eUnListen

    @staticmethod
    def GetType():
        return xx_connection.EConnectionType.eServer

    @staticmethod
    def GetDispathcerType():
        import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher
        return xx_dispatcher.EDispatcherType.eBuffer

    @staticmethod
    def GetConnectionType():
        return xx_connection.EConnectionType.eClient

    def Listen(self, szIp, nPort):
        if self.m_eConnectState == xx_connection.EConnectionState.eListening:
            self.m_LoggerObj.error("the connection is already listening, id:%d, ip:%s, port:%d, ListenCount:%d", self.ID, szIp, nPort, self.m_nListenCount)
            return False

        assert self.m_eConnectState == xx_connection.EConnectionState.eUnListen

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Listen(self.ID, szIp, nPort, self.m_nListenCount)

        self.m_eConnectState = xx_connection.EConnectionState.eListening

    def _Accept(self, SocketObj, szIp, nPort):
        import common.async_net.xx_connection_mgr as xx_connection_mgr

        nConnectionType = self.GetConnectionType()

        ClientConnectionObj = xx_connection_mgr.CreateConnection(nConnectionType)
        ClientConnectionObj.SetSocket(SocketObj)

        xx_connection_mgr.F_OnConnect(ClientConnectionObj.ID)

        return ClientConnectionObj
