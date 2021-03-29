import common.my_log as my_log
import main_frame.cmd_base as cmd_base

g_dictUUID2State = {}


class CmdDisTask(cmd_base.CmdBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "dis_task"

    def _OnInit(self):
        pass

    def Do(self):
        """执行命令"""
        self.m_LoggerObj.info("Start")

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
        while not xx_connection_mgr.IsConnected(nConnectionID):
            self.m_LoggerObj.info("wait to connect ...")

            time.sleep(1)
            xx_connection_mgr.Update()

        # call rpc
        import uuid
        import logic.connection.message_dispatcher as message_dispatcher

        szTaskUuid = uuid.uuid1()
        dictTaskData = {
            "uuid": szTaskUuid,
            "command": [
                "{{exe_fpath}} {{tga_file}} {{temp_dir}}  -s fast -c etc2 -f RGBA -ktx"
            ],
            "var": {
                "exe_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/etcpack.exe",
                },
                "tga_file": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.tga",
                },
                "temp_dir": {
                    "type": "dir",
                    "iot": "temp",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.ktx",
                },
                "ktx_file": {
                    "type": "file",
                    "iot": "output",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/cqs_ground_06.ktx/cqs_ground_06.ktx",
                }
            },
        }

        message_dispatcher.CallRpc(nConnectionID, "logic.gm.gm_command", "AddDisTask", [dictTaskData])

        # wait to do task
        while szTaskUuid not in g_dictUUID2State:
            self.m_LoggerObj.info("wait to do task ...")

            time.sleep(10)
            xx_connection_mgr.Update()

        self.m_LoggerObj.info("task finish!, dictTaskData:%s", Str(dictTaskData))

        # destroy
        time.sleep(1)
        xx_connection_mgr.DestroyConnection(nConnectionID)

        time.sleep(1)
        xx_connection_mgr.Update()

        xx_connection_mgr.Destroy()
