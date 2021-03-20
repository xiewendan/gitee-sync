import logging
import os
import unittest

from common.file_cache_system import FileCacheSystem


class TestMailMgr(unittest.TestCase):
    def setUp(self):
        logging.getLogger("myLog").debug("TestMailMgr setUp:")

    def test_file_cache_system(self):
        szRootPath = g_TestAppObj.ConfigLoader.CWD + "/data/cache_system"
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

        # 第一次，创建对象，并将三个文件放进去。最后一个文件放进去的时候，空间不够，需要删除第一个文件
        FileCacheSystemObj = FileCacheSystem(szRootPath, 70000)  # 单位为byte，这里是70K
        for listData in listFileData:
            szMd5 = listData[0]
            szFileName = listData[1]
            nSize = listData[2]
            szSrcFPath = listData[3]

            if not FileCacheSystemObj.CheckExistSameFile(szMd5, szFileName, nSize):
                FileCacheSystemObj.SaveFile(szMd5, szFileName, nSize, szSrcFPath)  # 没有的话，可以把文件存储进去
            else:
                FileCacheSystemObj.UseFile(szMd5, szFileName, nSize)
            assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == szMd5

        FileCacheSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

        # # 当前文件和索引状态
        FileCacheSystemObj = FileCacheSystem(szRootPath, 70000)  # 单位为byte，这里是70K
        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[1][0]
        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[2][0]

        assert not os.path.exists(FileCacheSystemObj._GenFPath(listFileData[0][0]))
        assert os.path.exists(FileCacheSystemObj._GenFPath(listFileData[1][0]))
        assert os.path.exists(FileCacheSystemObj._GenFPath(listFileData[2][0]))
        #
        # # 使用第二个文件，索引状态变化
        FileCacheSystemObj.UseFile(listFileData[1][0], listFileData[1][1], listFileData[1][2])
        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[2][0]
        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[1][0]

        FileCacheSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

        FileCacheSystemObj = FileCacheSystem(szRootPath, 70000)  # 单位为byte，这里是70K
        # 将第一个文件再放入
        assert not FileCacheSystemObj.CheckExistSameFile(listFileData[0][0], listFileData[0][1], listFileData[0][2])
        FileCacheSystemObj.SaveFile(listFileData[0][0], listFileData[0][1], listFileData[0][2], listFileData[0][3])

        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj.Top() == listFileData[1][0]
        assert FileCacheSystemObj.m_IndexMgrObj.m_LinkMd5QueueObj._Tail() == listFileData[0][0]

        assert os.path.exists(FileCacheSystemObj._GenFPath(listFileData[0][0]))
        assert os.path.exists(FileCacheSystemObj._GenFPath(listFileData[1][0]))
        assert not os.path.exists(FileCacheSystemObj._GenFPath(listFileData[2][0]))

        FileCacheSystemObj.Destroy()  # 销毁流程，会保持缓存系统的索引文件

    def tearDown(self):
        logging.getLogger("myLog").debug("TestMailMgr tearDown\n\n\n")
