import common.async_net.connection.xx_connection_server as xx_connection_server


class RegisterServerConnection(xx_connection_server.XxConnectionServer):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eRegisterServer

    @staticmethod
    def GetConnectionType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eExecutorInRegister

