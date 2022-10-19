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

    @staticmethod
    def _CreateTaskData(szTagFile):

        import uuid
        szTaskUuid = str(uuid.uuid1())

        import common.my_path as my_path
        szFileName = my_path.FileName(szTagFile)

        return {
            "uuid": szTaskUuid,
            "command": [
                "{{exe_fpath}} {{tga_file}} {{temp_dir}}  -s fast -c etc2 -f RGBA -ktx"
            ],
            "var": {
                "exe_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/etcpack.exe",
                    "rpath": "etcpack.exe",
                },
                "tga_file": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/" + szTagFile,
                    "rpath": szTagFile,
                },
                "convert_fpath": {
                    "type": "file",
                    "iot": "input",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/convert.exe",
                    "rpath": "convert.exe",
                },
                "temp_dir": {
                    "type": "dir",
                    "iot": "temp",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/%s.ktx" % szFileName,
                    "rpath": "%s.ktx" % szFileName,
                },
                "ktx_file": {
                    "type": "file",
                    "iot": "output",
                    "fpath": "E:/project/xiewendan/tools/template/data/test/%s.ktx/%s.ktx" % (szFileName, szFileName),
                    "rpath": "%s.ktx/%s.ktx" % (szFileName, szFileName)
                }
            },
        }

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
        import logic.connection.message_dispatcher as message_dispatcher

        listTga = [
            "card003_mfst_eyes01.tga",
            "card003_mfst_face01.tga",
            "cqs_ground_06.tga",
            "fx_shanfeng.tga",
            "fx_shanfeng_01.tga",
            "fxdragon_demo_101_02_d.tga",
            "kp_linshengchuan_face_01.tga",
            "kp_linshengchuan_hair_01.tga",
            "kp_linshengchuan_hair_d.tga",
            "kp_linshengchuan_hair_l.tga",
            "kp_linshengchuan_weapon.tga",
            "kp_linshengchuan_weapon_01.tga",
            "kp_linshengchuan_weapon_l.tga"
        ]

        for szTgaFile in listTga:
            dictTaskData = self._CreateTaskData(szTgaFile)

            message_dispatcher.CallRpc(nConnectionID, "logic.gm.gm_command", "AddDisTask", [dictTaskData])
            g_dictUUID2State[dictTaskData["uuid"]] = True

        # wait to do task
        while len(g_dictUUID2State) > 0:
            self.m_LoggerObj.info("wait to do task ...")

            time.sleep(1)
            xx_connection_mgr.Update()

        self.m_LoggerObj.info("task finish!")

        # destroy
        time.sleep(1)
        xx_connection_mgr.DestroyConnection(nConnectionID)

        time.sleep(1)
        xx_connection_mgr.Update()

        xx_connection_mgr.Destroy()
