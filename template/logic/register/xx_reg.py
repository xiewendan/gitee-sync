# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

import common.async_net.connection.xx_connection_server as xx_connection_server


class XxReg(xx_connection_server.XxConnectionServer):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eReg

    @staticmethod
    def GetConnectionType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eExeInReg
