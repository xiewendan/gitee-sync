# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/5/28 13:10

# desc:


import common.async_net.xx_connection_mgr as xx_connection_mgr
import common.lru_link_queue as lru_link_queue


class XxConnectionPool:
    """"""

    def __init__(self, nMaxCount=20):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_nMaxCount = nMaxCount
        self.m_nCurCount = 0

        self.m_dictTypeIpPort2ConnectionID = {}

        self.m_LRULinkQueueObj = lru_link_queue.LRULinkQueue()

    def _PopConnection(self, eType, szIp, nPort):
        self.m_nCurCount -= 1

        nConnectionID = self.m_dictTypeIpPort2ConnectionID[eType][szIp][nPort]
        self.m_LRULinkQueueObj.Pop(nConnectionID)

        del self.m_dictTypeIpPort2ConnectionID[eType][szIp][nPort]
        if len(self.m_dictTypeIpPort2ConnectionID[eType][szIp]) == 0:
            del self.m_dictTypeIpPort2ConnectionID[eType][szIp]

            if len(self.m_dictTypeIpPort2ConnectionID[eType]) == 0:
                del self.m_dictTypeIpPort2ConnectionID[eType]

    def _PushConnection(self, eType, szIp, nPort):
        self.m_nCurCount += 1
        nConnectionID = self.m_dictTypeIpPort2ConnectionID[eType][szIp][nPort]
        self.m_LRULinkQueueObj.Push(nConnectionID)

        if self.m_nCurCount > self.m_nMaxCount:
            nPopConnectionID = self.m_LRULinkQueueObj.Pop()
            self.m_nCurCount -= 1
            xx_connection_mgr.DestroyConnection(nPopConnectionID)

    def GetConnection(self, eType, szIp, nPort, dictData):
        self.m_LoggerObj.debug("type:%d, ip:%s, port:%d", eType, szIp, nPort)
        if eType in self.m_dictTypeIpPort2ConnectionID and szIp in self.m_dictTypeIpPort2ConnectionID[eType] and \
                nPort in self.m_dictTypeIpPort2ConnectionID[eType][szIp]:

            nConnectionID, dictDataObj = self.m_dictTypeIpPort2ConnectionID[eType][szIp][nPort]

            self._PopConnection(eType, szIp, nPort)

            if dictDataObj == dictData:
                if not xx_connection_mgr.IsConnected(nConnectionID):
                    xx_connection_mgr.Connect(szIp, nPort)
                return nConnectionID

            else:
                xx_connection_mgr.DestroyConnection(nConnectionID)

        nNewConnID = xx_connection_mgr.CreateConnection(eType, dictData)
        xx_connection_mgr.Connect(nNewConnID, szIp, nPort)

        return nNewConnID

    def PutConnection(self, eType, szIp, nPort, dictData, nConnectionID):
        self.m_LoggerObj.debug("type:%d, ip:%s, port:%d, connectionid:%d", eType, szIp, nPort, nConnectionID)

        if eType not in self.m_dictTypeIpPort2ConnectionID:
            self.m_dictTypeIpPort2ConnectionID[eType] = {}

        if szIp not in self.m_dictTypeIpPort2ConnectionID[eType]:
            self.m_dictTypeIpPort2ConnectionID[eType][szIp] = {}

        self.m_dictTypeIpPort2ConnectionID[eType][szIp][nPort] = (nConnectionID, dictData)

        self._PushConnection(eType, szIp, nPort)


g_XxConnectionPoolObj = XxConnectionPool()

GetConnection = g_XxConnectionPoolObj.GetConnection
PutConnection = g_XxConnectionPoolObj.PutConnection
