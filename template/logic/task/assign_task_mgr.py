class AssignTaskMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_listAssign = []

    def AddTask(self, dictData):
        # TODO 检查是否有重复的，是否会存在
        self.m_LoggerObj.info("dictData:%s", Str(dictData))

        self.m_listAssign.append(dictData)

    def Update(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        import common.async_net.connection.xx_connection as xx_connection
        import logic.connection.message_dispatcher as message_dispatcher

        listConnID = xx_connection_mgr.FilterConnIDList(xx_connection.EConnectionType.eExeInReg)

        nLenConnID = len(listConnID)

        if nLenConnID <= 1:
            self.m_LoggerObj.debug("executor not enough, count:%d", nLenConnID)
            return

        import random
        nIndex = random.randint(0, nLenConnID - 1)

        for dictData in self.m_listAssign:
            nRandomConnID = listConnID[nIndex]
            if nRandomConnID == dictData["conn_id"]:
                nIndex = self._AddIndex(nIndex, nLenConnID)
                nRandomConnID = listConnID[nIndex]

            assert nRandomConnID != listConnID[nIndex]  # 如果只有一个连接，肯定有问题
            message_dispatcher.CallRpc(nRandomConnID, "logic.gm.gm_command", "OnRecvAcceptTask", [dictData])

            nIndex = self._AddIndex(nIndex, nLenConnID)

        self.m_listAssign = []

    def _AddIndex(self, nIndex, nLen):
        nIndex += 1

        if nIndex >= nLen:
            nIndex = 0

        return nIndex


g_AssignTaskMgr = AssignTaskMgr()
AddTask = g_AssignTaskMgr.AddTask
Update = g_AssignTaskMgr.Update
