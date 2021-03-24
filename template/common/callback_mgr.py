class CallbackMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_nCbID = 0
        self.m_dictCb = {}

    def _GenCbID(self):
        self.m_nCbID += 1
        return self.m_nCbID

    def HasKey(self, nCbID):
        return nCbID in self.m_dictCb

    # TODO tuplearg，写法改为*
    def CreateCb(self, funCb, tupleArg):
        nCbID = self._GenCbID()
        assert nCbID not in self.m_nCbID
        self.m_dictCb[nCbID] = (funCb, tupleArg)

    def Call(self, nCbID, **kwargs):
        self.m_LoggerObj.debug("CbID:%d", nCbID)
        assert nCbID in self.m_nCbID

        funCb, tupleArg = self.m_dictCb[nCbID]
        funCb(*tupleArg, **kwargs)

        del self.m_dictCb[nCbID]


g_CallbackMgr = CallbackMgr()
HasKey = g_CallbackMgr.HasKey
CreateCb = g_CallbackMgr.CreateCb
Call = g_CallbackMgr.Call
