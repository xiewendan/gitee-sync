import common.async_net.connection.xx_connection_base as xx_connection_base
import common.async_net.connection.xx_connection as xx_connection
import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher


class XxConnectionServer(xx_connection_base.XxConnectionBase):
    """"""

    def __init__(self, dictConnectionData):
        super().__init__(dictConnectionData)

        self.m_nListenCount = dictConnectionData["socket_listen"]

    @staticmethod
    def GetType():
        return xx_connection.EConnectionType.eServer

    @staticmethod
    def GetDispathcerType():
        return xx_dispatcher.EDispatcherType.eBuffer

    def Listen(self, szIp, nPort):
        DispatcherObj = self._GetDispatcher()
        DispatcherObj.SetReuseAddress()
        DispatcherObj.Bind(szIp, nPort)
        DispatcherObj.Listen(self.m_nListenCount)
