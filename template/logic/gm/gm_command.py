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


g_GmCommandMgr = GmCommandMgr()
Do = g_GmCommandMgr.Do
AddOutput = g_GmCommandMgr.AddOutput
