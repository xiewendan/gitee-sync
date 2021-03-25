import logging
import os
import unittest


class TestDownloadSystem(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestDownloadSystem setUp:")

    def test_download_system(self):
        szRootPath = g_TestAppObj.ConfigLoader.CWD + "/data/download_system"
        listFileData = [
            [
                "9767f3103c55c66cc2c9eb39d56db594",
                "1.exe",
                28160,
                g_TestAppObj.ConfigLoader.CWD + "/unit_test/test_data/file_cache_system/1.data",
            ],
            [
                "a9c8c9a4f201a780d91eb9a426e3d930",
                "2.exe",
                28162,
                g_TestAppObj.ConfigLoader.CWD + "/unit_test/test_data/file_cache_system/2.data",
            ],
            [
                "97b9d60f3e36d64809844d4d034ba6be",
                "3.exe",
                28169,
                g_TestAppObj.ConfigLoader.CWD + "/unit_test/test_data/file_cache_system/3.data",
            ],
        ]

        def FunCB(name, nvalue, bOk=False):
            print("==============", name, nvalue, bOk)

        import common.callback_mgr as callback_mgr

        import common.download_system.download_system as download_system
        download_system.g_nMaxTotalSize = 70000

        # 第一次，创建对象，并将三个文件放进去。最后一个文件放进去的时候，空间不够，需要删除第一个文件
        DownloadSystemObj = download_system.DownloadSystem(szRootPath, 70000, nOverMilliSecond=1000)
        for listData in listFileData:
            szMd5 = listData[0]
            szFileName = listData[1]
            nSize = listData[2]
            szSrcFPath = listData[3]

            if not DownloadSystemObj.m_IndexMgrObj._CheckExist(szMd5, szFileName, nSize):
                nCbID = callback_mgr.CreateCb(FunCB, "xjc", 1)
                print(DownloadSystemObj.Download(szMd5, szFileName, nSize, nCbID))  # 没有的话，可以把文件存储进去
            else:
                DownloadSystemObj.UseFile(szMd5, szFileName, nSize)

            assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == szMd5

        DownloadSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

        # # 当前文件和索引状态
        DownloadSystemObj = download_system.DownloadSystem(szRootPath, 70000, nOverMilliSecond=1000)  # 单位为byte，这里是70K
        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[1][0]
        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[2][0]

        assert not os.path.exists(DownloadSystemObj._GenFPath(listFileData[0][0]))
        assert os.path.exists(DownloadSystemObj._GenFPath(listFileData[1][0]))
        assert os.path.exists(DownloadSystemObj._GenFPath(listFileData[2][0]))
        #
        # # 使用第二个文件，索引状态变化
        DownloadSystemObj.UseFile(listFileData[1][0], listFileData[1][1], listFileData[1][2])
        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[2][0]
        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[1][0]

        DownloadSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

        DownloadSystemObj = download_system.DownloadSystem(szRootPath, 70000, nOverMilliSecond=1000)  # 单位为byte，这里是70K
        # 将第一个文件再放入
        assert not DownloadSystemObj.m_IndexMgrObj._CheckExist(listFileData[0][0], listFileData[0][1], listFileData[0][2])
        nCbID = callback_mgr.CreateCb(FunCB, "xjc", 1)
        DownloadSystemObj.Download(listFileData[0][0], listFileData[0][1], listFileData[0][2], nCbID)

        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[1][0]
        assert DownloadSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[0][0]

        assert os.path.exists(DownloadSystemObj._GenFPath(listFileData[0][0]))
        assert os.path.exists(DownloadSystemObj._GenFPath(listFileData[1][0]))
        assert not os.path.exists(DownloadSystemObj._GenFPath(listFileData[2][0]))

        # 超时
        import time
        time.sleep(2)
        DownloadSystemObj.CheckOvertime()
        dictFileIndex = DownloadSystemObj.m_IndexMgrObj.GetAllFileIndex()
        for szMd5, FileIndexObj in dictFileIndex.items():
            assert len(FileIndexObj.GetCbList()) == 0

        DownloadSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

    def tearDown(self):
        logging.getLogger("myLog").debug("TestDownloadSystem tearDown\n\n\n")
