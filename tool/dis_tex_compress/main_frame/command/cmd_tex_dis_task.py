import re

import common.my_log as my_log
import common.my_path as my_path
import main_frame.cmd_base as cmd_base

g_dictUUID2State = {}

# 命令
# python main_frame/main.py "c:/PVRTexTool -shh -flip y -f PVRTC1_2_RGB -q pvrtcbest -i c:/Temp/aee4667d49fab44e7b1666ab4710dc60-feed.png -o c:/Temp/aee4667d49fab44e7b1666ab4710dc60-res.pvr"

class CmdTexDisTask(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "tex_dis_task"

    def _OnInit(self):
        pass

    def _CreateTaskData(self, szCompressCommand):
        self.m_LoggerObj.debug("compress command:%s", szCompressCommand)

        import uuid
        szTaskUuid = str(uuid.uuid1())

        szRegFormat = r"^([a-zA-Z0-9./ _:]+PVRTexTool) [a-zA-Z0-9_ -]* -i ([a-zA-Z0-9-./ _:]+) -o ([a-zA-Z0-9-./ _:]+.pvr)$"

        MatchObj = re.match(szRegFormat, szCompressCommand)
        if MatchObj is None:
            self.m_LoggerObj.error("compress command match re error: %s, %s", szCompressCommand, szRegFormat)
            return None

        szExeFPath, szImagFPath, szPvrFPath = MatchObj.groups()

        szCurCompressCommand = szCompressCommand.replace(szExeFPath, "{{exe_fpath_{{platform}}}}"). \
            replace(szImagFPath, "{{image_fpath}}"). \
            replace(szPvrFPath, "{{pvr_fpath}}")

        dictPlatformExePath = self._CreatePlatformVar("exe_fpath", szExeFPath, ["windows", "darwin", "linux"])
        dictVar = {
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
        }
        dictVar.update(dictPlatformExePath)

        dictRet = {
            "uuid": szTaskUuid,
            "command": [
                "chmod +x {{exe_fpath_{{platform}}}}",
                szCurCompressCommand
            ],
            "var": dictVar,
        }

        self.m_LoggerObj.info("dict command:%s", str(dictRet))

        return dictRet

    @staticmethod
    def _CreatePlatformVar(szVarName, szFPath, listPlatform):
        dictVar = {}
        for szPlatform in listPlatform:
            szPlatformVarName = "%s_%s" % (szVarName, szPlatform)
            szPlatformFPath = "%s.%s" % (szFPath, szPlatform)
            dictVar[szPlatformVarName] = {
                "type": "file",
                "iot": "input",
                "platform": szPlatform,
                "fpath": szPlatformFPath,
                "rpath": my_path.FileNameWithExt(szPlatformFPath),
            }

        return dictVar

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

        szCompressCommand = self.m_AppObj.CLM.GetArg(1)

        import logic.connection.message_dispatcher as message_dispatcher

        dictTaskData = self._CreateTaskData(szCompressCommand)

        if dictTaskData is None:
            self.m_LoggerObj.error("compress error, compress command:%s", szCompressCommand)
            return

        import time
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection

        dictConnectionData = xx_connection_mgr.CreateConnectionData()

        nConnectionID = xx_connection_mgr.CreateConnection(
            xx_connection.EConnectionType.eClient,
            dictConnectionData)

        # connect
        xx_connection_mgr.Connect(nConnectionID, "127.0.0.1", 60000)

        # wait connect
        while not xx_connection_mgr.IsConnected(nConnectionID):
            self.m_LoggerObj.info("wait to connect ...")

            time.sleep(1)
            xx_connection_mgr.Update()

        # call rpc
        message_dispatcher.CallRpc(nConnectionID, "logic.gm.gm_command", "AddDisTask", [dictTaskData])
        g_dictUUID2State[dictTaskData["uuid"]] = True

        # wait to do task
        nWaitingCount = 600
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
