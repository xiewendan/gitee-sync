import re

import common.my_log as my_log
import common.my_path as my_path
import main_frame.cmd_base as cmd_base

g_dictUUID2State = {}


class CmdDisTask(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "unity_tex_dis_task"

    def _OnInit(self):
        pass

    def _CreateTaskData(self, szUnityProjectDir, szCompressCommand):
        self.m_LoggerObj.debug("unity project dir:%s, compress command:%s", szUnityProjectDir, szCompressCommand)

        import uuid
        szTaskUuid = str(uuid.uuid1())

        szRegFormat = r"^([a-zA-Z0-9./]+PVRTexTool_orig) [a-zA-Z0-9_ -]* -i (Temp/[a-zA-Z0-9-.]+) -o (Temp/[a-zA-Z0-9-]+.pvr)$"

        MatchObj = re.match(szRegFormat, szCompressCommand)
        if MatchObj is None:
            return None

        szExeFPath, szImageRPath, szPvrRPath = MatchObj.groups()

        szImagFPath = szUnityProjectDir + "/" + szImageRPath
        szPvrFPath = szUnityProjectDir + "/" + szPvrRPath

        szCurCompressCommand = szCompressCommand.replace(szExeFPath, "{{exe_fpath{{platform}}}}"). \
            replace(szImageRPath, "{{image_fpath}}"). \
            replace(szPvrRPath, "{{pvr_fpath}}")

        dictPlatformExePath = self._CreatePlatformVar("exe_fpath", szExeFPath, ["windows, darwin"])

        dictRet = {
            "uuid": szTaskUuid,
            "command": [
                "chmod +x {{exe_fpath{{platform}}}}",
                szCurCompressCommand
            ],
            "var": {
                "image_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": szImagFPath,
                    "rpath": my_path.FileNameWithExt(szImagFPath)
                },
                "pvr_fpath": {
                    "type": "file",
                    "iot": "output",
                    "fpath": szPvrFPath,
                    "rpath": my_path.FileNameWithExt(szPvrFPath)
                },
            }.update(dictPlatformExePath),
        }
        self.m_LoggerObj.info("dict command:%s", str(dictRet))

        return dictRet

    @staticmethod
    def _CreatePlatformVar(szVarName, szFPath, listPlatform):
        dictVar = {}
        for szPlatform in listPlatform:
            szPlatformVarName = "%s.%s" % (szVarName, szPlatform)
            szPlatformFPath = "%s.%s" % (szFPath, szPlatform)
            dictVar[szPlatformVarName] = {
                "type": "file",
                "iot": "input",
                "platform": "windows",
                "fpath": szPlatformFPath,
                "rpath": my_path.FileNameWithExt(szPlatformFPath),
            }

        return dictVar

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szTargetIp = self.m_AppObj.CLM.GetArg(1)
        nTargetPort = int(self.m_AppObj.CLM.GetArg(2))
        szUnityProjectDir = self.m_AppObj.CLM.GetArg(3)
        szCompressCommand = self.m_AppObj.CLM.GetArg(4)

        import logic.connection.message_dispatcher as message_dispatcher

        dictTaskData = self._CreateTaskData(szUnityProjectDir, szCompressCommand)

        if dictTaskData is None:
            self.m_LoggerObj.error("compress error, project dir:%s, compress command:%s", szUnityProjectDir, szCompressCommand)
            return

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
        while not xx_connection_mgr.IsConnected(nConnectionID):
            self.m_LoggerObj.info("wait to connect ...")

            time.sleep(1)
            xx_connection_mgr.Update()

        # call rpc
        message_dispatcher.CallRpc(nConnectionID, "logic.gm.gm_command", "AddDisTask", [dictTaskData])
        g_dictUUID2State[dictTaskData["uuid"]] = True

        # wait to do task
        nWaitingCount = 300
        while len(g_dictUUID2State) > 0 and nWaitingCount > 0:
            self.m_LoggerObj.info("wait to do task ...: %d", nWaitingCount)

            time.sleep(1)
            nWaitingCount -= 1
            xx_connection_mgr.Update()

        self.m_LoggerObj.info("task finish!")

        # destroy
        time.sleep(1)
        xx_connection_mgr.DestroyConnection(nConnectionID)

        time.sleep(1)
        xx_connection_mgr.Update()

        xx_connection_mgr.Destroy()
