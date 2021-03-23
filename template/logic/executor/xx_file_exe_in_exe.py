import common.async_net.connection.xx_connection_base as xx_connection_base


class XxFileExeInExe(xx_connection_base.XxConnectionBase):
    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eFileExeInExe

    @staticmethod
    def GetDispathcerType():
        import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher
        return xx_dispatcher.EDispatcherType.eBuffer
