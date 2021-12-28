# -*- coding: utf-8 -*-
# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:


import socket
import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdExecutor(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "executor"

    def _OnInit(self):
        pass

    def GetListenIp(self):
          try:
              s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              s.connect(("8.8.8.8",8))
              ip=s.getsockname()[0]
          finally:
              s.close()
    
          return ip

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szBaseFPath = "%s/%s" % (szCWD, self.m_AppObj.CLM.GetArg(1))
        szBaseFPath.replace("\\", "/")

        szRegisterIp = self.m_AppObj.CLM.GetArg(2)
        nRegisterPort = int(self.m_AppObj.CLM.GetArg(3))
        szListenIp = self.GetListenIp()
        nListenPort = int(self.m_AppObj.CLM.GetArg(4))
        nFilePort = int(self.m_AppObj.CLM.GetArg(5))

        dictData = {
            "register_ip": szRegisterIp,
            "register_port": nRegisterPort,
            "listen_ip": szListenIp,
            "listen_port": nListenPort,
            "file_listen_ip": szListenIp,
            "file_listen_port": nFilePort,
        }

        import common.download_system.download_system as download_system
        download_system.Init(szBaseFPath + "/download_system")

        import common.file_cache_system.file_cache_system as file_cache_system
        file_cache_system.Init(szBaseFPath + "/cache_system")

        import logic.executor.executor as executor
        ExecutorObj = executor.Executor(dictData)
        ExecutorObj.Run()
