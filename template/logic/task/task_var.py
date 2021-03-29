import logic.task.task_enum as task_enum
class TaskVar:
    """"""

    def __init__(self, szName: str, nType, nIotType, szFPath):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_LoggerObj.debug("name:%s, type:%d, iot_type:%d, fpath:%s", szName, nType, nIotType, szFPath)

        self.m_szName = szName
        self.m_nType = nType
        self.m_nIotType = nIotType
        self.m_szFPath = szFPath

        self.m_szMd5 = ""
        self.m_nSize = 0
        self.m_szFileName = ""

    def Init(self):
        import os
        import common.md5 as md5
        import common.my_path as my_path

        self.m_szMd5 = md5.GetFileMD5(self.m_szFPath)
        self.m_nSize = os.path.getsize(self.m_szFPath)
        self.m_szFileName = my_path.FileNameWithExt(self.m_szFPath)

        self.m_LoggerObj.info("md5:%s, size:%d, filename:%s", self.m_szMd5, self.m_nSize, self.m_szFileName)

    def IsInput(self):
        return self.m_nIotType == task_enum.EIotType.eInput

    def IsOutput(self):
        return self.m_nIotType == task_enum.EIotType.eOutput

    def IsTemp(self):
        return self.m_nIotType == task_enum.EIotType.eTemp
