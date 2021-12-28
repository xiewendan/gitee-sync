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
        return "executor_k8s"

    def _OnInit(self):
        pass

    def GetRegisterIp(self, szServiceName):
        import time

        for i in range(60):
            try:
                self.m_LoggerObj.info("try get register ip of service %s: %d", szServiceName, i)
                szHost = socket.gethostbyname(szServiceName)
                return szHost
            except socket.gaierror:
                time.sleep(1)
        
        import common.my_exception as my_exception
        raise my_exception.MyException("gethostbyname error" + szServiceName)

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
        self.m_LoggerObj.info("Start")

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szRegisterIp = self.GetRegisterIp("dis-tex-register")
        nRegisterPort = 50000

        szListenIp = self.GetListenIp()
        nListenPort = 60000
        nFilePort = 60001
        szTempFPath = self.m_AppObj.CLM.GetArg(1)
        szTempFPath.replace("\\", "/")

        import common.path_mgr.path_mgr as path_mgr
        path_mgr.SetTemp(szTempFPath)

        self.m_LoggerObj.info("arg parse succeed, register ip: %s, listen ip: %s", szRegisterIp, szListenIp)

        dictData = {
            "register_ip": szRegisterIp,
            "register_port": nRegisterPort,
            "listen_ip": szListenIp,
            "listen_port": nListenPort,
            "file_listen_ip": szListenIp,
            "file_listen_port": nFilePort,
        }

        import common.download_system.download_system as download_system
        download_system.Init(szTempFPath + "/download_system")

        import common.file_cache_system.file_cache_system as file_cache_system
        file_cache_system.Init(szTempFPath + "/cache_system")

        import logic.executor.executor as executor
        ExecutorObj = executor.Executor(dictData)
        ExecutorObj.Run()
