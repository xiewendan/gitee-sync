# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:02

# desc: 自己的XxSocket对象

import common.my_log as my_log


class XxSocket:
    def __init__(self, SocketObj, szIp, nPort, nID, eType):
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_SocketObj = SocketObj

        self.m_szIp = szIp
        self.m_nPort = nPort

        self.m_nID = nID
        self.m_eType = eType

    @property
    def SocketObj(self):
        return self.m_SocketObj

    @property
    def Ip(self):
        return self.m_szIp

    @property
    def Port(self):
        return self.m_nPort

    @property
    def ID(self):
        return self.m_nID

    @property
    def Type(self):
        return self.m_eType
