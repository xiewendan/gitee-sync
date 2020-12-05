# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import time
import threading
import socket
import main_frame.cmd_base as cmd_base


class CmdNetServer(cmd_base.CmdBase):
    def __init__(self):
        self.m_AppObj = None

    @staticmethod
    def GetName():
        return "net_server"

    def SocketThread(self, ConnObj, szAddr):
        time.sleep(10)
        self.m_AppObj.Info("socket thread running, ip: %s", szAddr)
        while True:
            szRecvData = ConnObj.recv(1024)
            if len(szRecvData) == 0:
                self.m_AppObj.Info("socket disconnect: %s", szAddr)
                break

            self.m_AppObj.Info("socket data recv:%s", szRecvData.decode("utf-8"))

        ConnObj.close()

    def Do(self):
        self.m_AppObj.Info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))

        with socket.socket() as SocketObj:
            # SocketObj.setblocking(False)
            SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 250 * 1024)  # 250KB

            SocketObj.bind((szIP, nPort))
            SocketObj.listen(5)

            self.m_AppObj.Info("socket listen, backlog %d, ip %s, port %d", 5, szIP, nPort)

            while True:
                ConnObj, szAddr = SocketObj.accept()
                self.m_AppObj.Info("socket connect: %s", szAddr)
                SocketThreadObj = threading.Thread(target=self.SocketThread, args=(ConnObj, szAddr))
                SocketThreadObj.start()
                self.m_AppObj.Info("socket thread start run: %s", szAddr)






