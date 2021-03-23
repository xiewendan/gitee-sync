import common.async_net.connection.xx_connection as xx_connection
import common.async_net.connection.xx_connection_server as xx_connection_server


class XxExe(xx_connection_server.XxConnectionServer):

    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        return xx_connection.EConnectionType.eExe

    @staticmethod
    def GetConnectionType():
        return xx_connection.EConnectionType.eExeInExe
