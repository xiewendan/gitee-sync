# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

class GmCommandMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_listOutput = []

    def _ClearOutput(self):
        self.m_listOutput = []

    def AddOutput(self, szMsg):
        self.m_listOutput.append(szMsg)

    def Do(self, nID, szCommand):
        self.m_LoggerObj.debug("id:%d, command:%s", nID, szCommand)

        self._ClearOutput()

        exec(szCommand)

        szOutput = "\n".join(self.m_listOutput)
        self._ClearOutput()

        return {"ret": szOutput}


def TestDo():
    nIndex = 10
    nIndex += 20

    AddOutput("xjc")
    AddOutput(str(nIndex))


def GetAllExecutorData():
    import logic.register.executor_mgr as executor_mgr
    szExecutorData = executor_mgr.ExecutorDataToStr()

    AddOutput(szExecutorData)


def GetAllConnectionData():
    import common.async_net.xx_connection_mgr as xx_connection_mgr
    szData = xx_connection_mgr.GetAllDataStr()

    AddOutput(szData)


g_GmCommandMgr = GmCommandMgr()
Do = g_GmCommandMgr.Do
AddOutput = g_GmCommandMgr.AddOutput
