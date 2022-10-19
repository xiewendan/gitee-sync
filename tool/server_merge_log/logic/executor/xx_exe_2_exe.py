import common.async_net.connection.xx_connection_client as xx_connection_client


class XxExe2Exe(xx_connection_client.XxConnectionClient):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eExe2Exe
