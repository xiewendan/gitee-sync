# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc:

import json
import os
import socket
import struct
import threading
import time

import common.my_log as my_log
import common.stat_mgr as stat_mgr
import main_frame.cmd_base as cmd_base
import main_frame.command.test.cmd_net_client as cmd_net_client


class CmdNetServer(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "net_server"

    def _SocketThread(self, ConnObj, szAddr):
        import common.my_path as my_path
        self.m_LoggerObj.info("socket thread running, ip: %s", szAddr)

        StatMgrObj = stat_mgr.StatMgr()
        StatMgrObj.LogTimeTag("begin")

        bytesLen = ConnObj.recv(12)
        nTotalDataLen, nFileNameLen = struct.unpack("!QI", bytesLen)

        szFileName = ConnObj.recv(nFileNameLen).decode("utf-8")
        szUploadFPath = "%s/%s/%s" % (os.getcwd(), "data/uploads", szFileName)
        my_path.CreateFileDir(szUploadFPath)

        with open(szUploadFPath, "wb") as fwp:
            nRecvLen = 0

            while True:
                if nRecvLen + cmd_net_client.TCP_MAX_BYTE < nTotalDataLen:
                    szRecvData = ConnObj.recv(cmd_net_client.TCP_MAX_BYTE)
                    nRecvLen += len(szRecvData)
                elif nRecvLen + cmd_net_client.TCP_MAX_BYTE >= nTotalDataLen:
                    szRecvData = ConnObj.recv(nTotalDataLen - nRecvLen)
                    nRecvLen += len(szRecvData)
                else:
                    pass

                fwp.write(szRecvData)

                if nRecvLen == nTotalDataLen:
                    break

            self.m_LoggerObj.info("total szie:%d", nRecvLen)
            bytesSendLen = struct.pack("!Q", nRecvLen)
            ConnObj.send(bytesSendLen)

        ConnObj.close()

        StatMgrObj.LogTimeTag("end")
        print(StatMgrObj.GetTimeTagStat())
        self.m_LoggerObj.info("receive file:%s" % szUploadFPath)

        # 处理上传文件
        self._OnUploadFile(szUploadFPath)

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD

        szIP = self.m_AppObj.CLM.GetArg(1)
        nPort = int(self.m_AppObj.CLM.GetArg(2))

        with socket.socket() as SocketObj:
            # SocketObj.setblocking(False)
            # SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10240 * 1024)  # 250KB

            SocketObj.bind((szIP, nPort))
            SocketObj.listen(5)

            self.m_LoggerObj.info("socket listen, backlog %d, ip %s, port %d", 5, szIP, nPort)

            while True:
                ConnObj, szAddr = SocketObj.accept()
                self.m_LoggerObj.info("socket connect: %s", szAddr)
                SocketThreadObj = threading.Thread(target=self._SocketThread, args=(ConnObj, szAddr))
                SocketThreadObj.start()
                self.m_LoggerObj.info("socket thread start run: %s", szAddr)

    def _OnUploadFile(self, szUploadFPath):
        self.m_LoggerObj.info("file name:%s" % szUploadFPath)

        import common.my_path as my_path

        if szUploadFPath.find("_") < 0:
            self.m_LoggerObj.debug("file name need not handle:%s" % szUploadFPath)
            return

        szUploadDir = my_path.ParseDir(szUploadFPath)
        szUploadFileNameNoExt = my_path.FileName(szUploadFPath)
        szScriptFunName, _ = szUploadFileNameNoExt.split("_")

        # 找到最近的一个时间点的文件
        szLastFileFPath = self._FindLastFile(szUploadDir, szUploadFileNameNoExt)

        self.m_LoggerObj.info(
            "callback name:%s, uploadfile:%s, lastfile:%s" % (szScriptFunName, szUploadFPath, szLastFileFPath))
        getattr(self, "_" + szScriptFunName)(szUploadFPath, szLastFileFPath)

    def _FindLastFile(self, szDir, szUploadFileNameNoExt):
        """找到上一个时间最近的文件"""
        self.m_LoggerObj.info("find dir:%s, upload file name:%s" % (szDir, szUploadFileNameNoExt))

        import common.my_path as my_path

        _, szUploadTime = szUploadFileNameNoExt.split("_")
        print(szUploadTime)
        nUploadSencods = time.mktime(time.strptime(szUploadTime, "%Y-%m-%d-%H-%M-%S"))

        nMaxLastFileSecond = 0
        szLastFileFPath = ""

        for szParentPath, listDirName, listFileName in os.walk(szDir):
            for szFileName in listFileName:
                szFileNameNoExt = my_path.FileName(szFileName)
                if szFileNameNoExt == szUploadFileNameNoExt:
                    continue

                if szFileNameNoExt.startswith("AutoProfile_"):
                    import common.my_path as my_path
                    szTime = szFileNameNoExt.split("_")[1]
                    nSeconds = time.mktime(time.strptime(szTime, "%Y-%m-%d-%H-%M-%S"))

                    if nSeconds > nUploadSencods:
                        continue

                    if nSeconds > nMaxLastFileSecond:
                        nMaxLastFileSecond = nSeconds
                        szLastFileFPath = os.path.join(szParentPath, szFileName)

        self.m_LoggerObj.info("last file:%s" % szLastFileFPath)
        return szLastFileFPath

    def _AutoProfile(self, szUploadFPath, szLastFileFPath):
        self.m_LoggerObj.info("uploadfile:%s, lastfile:%s" % (szUploadFPath, szLastFileFPath))

        assert os.path.exists(szUploadFPath), "文件不存在"

        if not os.path.exists(szLastFileFPath):
            self.m_LoggerObj.info("last file not exist: %s" % szLastFileFPath)
            return

        # 加载数据
        dictUploadData = json.load(open(szUploadFPath, "r"))
        dictLastData = json.load(open(szLastFileFPath, "r"))

        # 对比数据
        listCompareData = []
        listCompareData.append("%s -> %s<br>" % (szLastFileFPath, szUploadFPath))
        for szKey, ValueObj in dictUploadData.items():
            if isinstance(ValueObj, (dict, list)):
                assert False, "暂时不支持的值格式"
            else:
                listCompareData.append("%s:%s->%s" % (szKey, str(dictLastData.get(szKey, "")), str(ValueObj)))

        szCompareData = "\n".join(listCompareData)

        # 发送邮件
        # import common.notify as notify
        # notify.send_mail("jinchunxie@126.com", "[auto profile] compare data", szCompareData)
        self.m_LoggerObj.debug("mail_title:%s \ndata:%s" % ("[auto profile] compare data", szCompareData))
