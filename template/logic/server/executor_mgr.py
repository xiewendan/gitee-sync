# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

class ExecutorMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictExecutorData = {}

    def AddExecutorData(self, nConnID, dictData):
        self.m_LoggerObj.debug("ConnID:%d, dictData:%s", nConnID, str(dictData))

        assert nConnID not in self.m_dictExecutorData
        self.m_dictExecutorData[nConnID] = dictData

    def UpdateExecutorData(self, nConnID, dictData):
        self.m_LoggerObj.debug("ConnID:%d, dictData:%s", nConnID, dictData)

        assert nConnID in self.m_dictExecutorData

        for szKey, szValue in dictData.items():
            self.m_dictExecutorData[nConnID][szKey] = szValue

    def RemoveExecutorData(self, nConnID):
        self.m_LoggerObj.debug("ConnID:%d", nConnID)

        assert nConnID in self.m_dictExecutorData
        del self.m_dictExecutorData[nConnID]

    def ExecutorDataToStr(self):
        listRet = ["%8s %16s %6s %16s %12s" % ("ConnID", "ip", "port", "listen_ip", "listen_port")]

        szFormat = "%8d %16s %6s %16s %12s"

        for nConnID, dictData in self.m_dictExecutorData.items():
            szIp = dictData["ip"]
            nPort = dictData["port"]
            szListenIp = dictData.get("listen_ip", "")
            szListenPort = dictData.get("listen_port", "")

            listRet.append(szFormat % (nConnID, szIp, nPort, szListenIp, szListenPort))

        return "\n".join(listRet)


g_ExecutorMgr = ExecutorMgr()
AddExecutorData = g_ExecutorMgr.AddExecutorData
UpdateExecutorData = g_ExecutorMgr.UpdateExecutorData
RemoveExecutorData = g_ExecutorMgr.RemoveExecutorData
ExecutorDataToStr = g_ExecutorMgr.ExecutorDataToStr
