# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdTestCode(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "test_code"

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD
        szFilePath = self.m_AppObj.CLM.GetArg(1)
        szFileFullPath = "{0}/{1}".format(szCWD, szFilePath)

        import hashlib
        Md5Obj = hashlib.md5()

        with open(szFileFullPath, "rb") as FileObj:
            while True:
                szData = FileObj.read(1024)
                if szData == b'':
                    break
                Md5Obj.update(szData)

        print(Md5Obj.hexdigest())
