# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/23 22:15

# desc: 新的net网络


import threading

import common.my_log as my_log
import common.net.ip_port_data as ip_port_data


class XxNet:
    """网络接口"""

    def __init__(self):
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_listListenData = []  # [IpPortData,...]
        self.m_ListenLockObj = threading.Lock()

        self.m_listSendData = []  # [IpPortData,...]
        self.m_SendLockObj = threading.Lock()

        self.m_listRecvData = []  # [IpPortData,...]
        self.m_RecvLockObj = threading.Lock()

        import common.net.xx_socket_mgr as xx_socket_mgr
        self.m_XxSocketMgrObj = xx_socket_mgr.XxSocketMgr(self)
        self.m_XxSocketMgrObj.Start()

    def Destroy(self):
        self.m_XxSocketMgrObj.Destroy()

    def Listen(self, szIp, nPort):
        self.m_LoggerObj.info("ip:%s, port:%d", szIp, nPort)

        IpPortDataObj = ip_port_data.IpPortData(szIp, nPort)

        self.m_ListenLockObj.acquire()
        self.m_listListenData.append(IpPortDataObj)
        self.m_ListenLockObj.release()

    def Send(self, szIp, nPort, dictData):
        self.m_LoggerObj.info("ip:%s, port:%d, dictData:%s", szIp, nPort, str(dictData))

        IpPortDataObj = ip_port_data.IpPortData(szIp, nPort, dictData)

        self.m_SendLockObj.acquire()
        self.m_listSendData.append(IpPortDataObj)
        self.m_SendLockObj.release()

    def HandleRecv(self):
        self.m_LoggerObj.info("handle recv")

        self.m_RecvLockObj.acquire()
        listRecvData = self.m_listRecvData
        self.m_listRecvData = []
        self.m_RecvLockObj.release()

        for IpPortDataObj in listRecvData:
            szIp = IpPortDataObj.Ip
            nPort = IpPortDataObj.Port
            dictData = IpPortDataObj.Data

            self._Handle(szIp, nPort, dictData)

    def _Handle(self, szIp, nPort, dictData):
        self.m_LoggerObj.info("ip:%s, port:%d, data:%s", szIp, nPort, str(dictData))
        # TODO 需要在主程序里面处理数据
        pass

    def GetSendData(self):
        self.m_LoggerObj.info("get send data")

        self.m_SendLockObj.acquire()
        listSendData = self.m_listSendData
        self.m_listSendData = []
        self.m_SendLockObj.release()

        return listSendData

    def AddRecvData(self, listRecvData):
        self.m_LoggerObj.info("")

        self.m_RecvLockObj.acquire()
        self.m_listRecvData.extend(listRecvData)
        self.m_RecvLockObj.release()

    def GetListenData(self):
        self.m_LoggerObj.info("get listen data")

        self.m_ListenLockObj.acquire()
        listListenData = self.m_listListenData
        self.m_listListenData = []
        self.m_ListenLockObj.release()

        return listListenData
