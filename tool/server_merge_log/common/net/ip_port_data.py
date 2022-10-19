# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/23 23:55

# desc: ip_port数据封装


class IpPortData:
    """"""

    def __init__(self, szIp, nPort, dictData=None):
        self.m_szIp = szIp
        self.m_nPort = nPort
        self.m_dictData = dictData

    @property
    def Ip(self):
        return self.m_szIp

    @property
    def Port(self):
        return self.m_nPort

    @property
    def Data(self):
        return self.m_dictData
