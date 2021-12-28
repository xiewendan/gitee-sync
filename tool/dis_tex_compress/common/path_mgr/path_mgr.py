import os
class PathMgr:
    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_szTempFPath = "%s/data/temp" % (os.getcwd())
        self.m_LoggerObj.info("init szTempFPath:%s", self.m_szTempFPath)

    def SetTemp(self, szFPath):
        self.m_szTempFPath = szFPath
        self.m_LoggerObj.info("set szTempFPath:%s", self.m_szTempFPath)
    
    def GetTemp(self):
        return self.m_szTempFPath

g_PathMgr = PathMgr()
SetTemp = g_PathMgr.SetTemp
GetTemp = g_PathMgr.GetTemp