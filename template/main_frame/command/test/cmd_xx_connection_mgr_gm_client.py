# -*- coding: utf-8 -*-
# __author__ = xiaobao
# __date__ = 2021/2/4 12:08

# desc:


import common.my_log as my_log
import main_frame.cmd_base as cmd_base


class CmdXxConnectionMgrClient(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "xx_connection_mgr_gm_client"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        # szCWD = self.m_AppObj.ConfigLoader.CWD

        szTargetIp = self.m_AppObj.CLM.GetArg(1)
        nTargetPort = int(self.m_AppObj.CLM.GetArg(2))

        import time
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData()

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eClient,
            dictConnectionData)

        # connect
        xx_connection_mgr.Connect(nConnectionID, szTargetIp, nTargetPort)

        # wait connect
        nCount = 2
        while nCount > 0:
            time.sleep(1)
            xx_connection_mgr.Update()
            nCount -= 1

        # call rpc
        import logic.connection.message_dispatcher as message_dispatcher

        listCommand = [
            "\n".join(
                [
                    # 销毁连接
                    # "import common.async_net.xx_connection_mgr as xx_connection_mgr",
                    # "xx_connection_mgr.DestroyConnection(4)",

                    # 发起连接Exe
                    "import common.async_net.xx_connection_mgr as xx_connection_mgr",
                    "import common.async_net.connection.xx_connection as xx_connection",
                    "dictConnectionData = xx_connection_mgr.CreateConnectionData()",
                    "nConnectionID = xx_connection_mgr.CreateConnection(xx_connection.EConnectionType.eExe2Exe, dictConnectionData)",
                    "xx_connection_mgr.Connect(nConnectionID, '127.0.0.1', 60020)",
                    "dictConnectionData1 = xx_connection_mgr.CreateConnectionData()",
                    "nConnectionID1 = xx_connection_mgr.CreateConnection(xx_connection.EConnectionType.eFileExe2Exe, dictConnectionData1)",
                    "xx_connection_mgr.Connect(nConnectionID1, '127.0.0.1', 60021)",

                ]),
            "\n".join(
                [
                    # 下载文件
                    "import logic.gm.gm_command as gm_command",
                    "gm_command.DownloadFile()",
                ]),
            # "\n".join(
            #     [
            #         # 打印所有的数据
            #         "import logic.gm.gm_command as gm_command",
            #         "gm_command.GetAllConnectionData()",
            #         "gm_command.GetDownloadData()",
            #         "gm_command.GetAllExecutorData()",
            #     ]
            # )

        ]

        import time
        for szCommand in listCommand:
            def GMCallback(dictData):
                self.m_LoggerObj.info("********************dictData:%s", str(dictData))
                if "ret" in dictData:
                    self.m_LoggerObj.info("********************ret:\n%s", dictData["ret"])

            message_dispatcher.CallRpc(nConnectionID, "logic.gm.gm_command", "Do", [szCommand],
                                       Callback=GMCallback,
                                       tupleArg=())

            # wait callback
            nCount = 4
            while nCount > 0:
                time.sleep(1)
                xx_connection_mgr.Update()
                nCount -= 1

        # destroy
        time.sleep(1)
        xx_connection_mgr.DestroyConnection(nConnectionID)

        time.sleep(1)
        xx_connection_mgr.Update()

        xx_connection_mgr.Destroy()
