# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/4 20:56

# desc:

import common.net.xx_net as xx_net

__all__ = ("XxAsyncNet",)


class EAsyncName:
    eRetAsyncID = "RetAsyncID"
    eAsyncID = "AsyncID"


class XxAsyncNet(xx_net.XxNet):
    """"""

    def __init__(self):
        super().__init__()

        self.m_nAsyncID = 0
        self.m_dictAsyncID2Callback = {}

    def SendAsync(self, szIp, nPort, dictData, funCallback, tupleArg):
        self.m_LoggerObj.debug("ip:%s, port:%d, dictData:%s, arg:%s", szIp, nPort, str(dictData), str(tupleArg))

        nAsyncID = self._GenAsyncID()
        self._AddAsyncCallback(nAsyncID, funCallback, tupleArg)

        assert EAsyncName.eRetAsyncID not in dictData
        dictData[EAsyncName.eRetAsyncID] = nAsyncID

        self.Send(szIp, nPort, dictData)

    # ********************************************************************************
    # async callback
    # ********************************************************************************
    def _GenAsyncID(self):
        self.m_nAsyncID += 1
        return self.m_nAsyncID

    def _AddAsyncCallback(self, nAsyncID, funCallback, tupleArg):
        self.m_LoggerObj.debug("asyncid:%d, arg:%s", nAsyncID, str(tupleArg))

        assert nAsyncID not in self.m_dictAsyncID2Callback
        self.m_dictAsyncID2Callback[nAsyncID] = (funCallback, tupleArg)

    def _RemoveAsyncCallback(self, nAsyncID):
        self.m_LoggerObj.debug("asyncid:%d", nAsyncID)
        assert nAsyncID in self.m_dictAsyncID2Callback
        del self.m_dictAsyncID2Callback[nAsyncID]

    def _GetAsyncCallback(self, nAsyncID):
        self.m_LoggerObj.debug("asyncid:%d", nAsyncID)

        assert nAsyncID in self.m_dictAsyncID2Callback
        return self.m_dictAsyncID2Callback[nAsyncID]

    def _Handle(self, szIp, nPort, dictData):
        self.m_LoggerObj.debug("ip:%s, port:%d, dictData:%s", szIp, nPort, str(dictData))

        if EAsyncName.eAsyncID in dictData:
            nAsyncID = dictData[EAsyncName.eAsyncID]
            self.m_LoggerObj.debug("call asyncid:%d", nAsyncID)
            funCallback, tupleArg = self._GetAsyncCallback(nAsyncID)
            funCallback(*tupleArg)
        else:
            # 处理逻辑
            pass

        if EAsyncName.eRetAsyncID in dictData:
            nRetAsyncID = dictData[EAsyncName.eRetAsyncID]
            self.m_LoggerObj.debug("send ret asyncid:%d", nRetAsyncID)
            self.Send(szIp, nPort, {EAsyncName.eAsyncID: nRetAsyncID})

        pass
