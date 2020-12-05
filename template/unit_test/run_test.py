# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/08/08 12:30:42

# desc: desc

import os
import sys
import unittest
import logging
import logging.config
import builtins


def CheckCWD():
    print(os.getcwd())
    szMainFilePath = os.getcwd() + "/unit_test/run_test.py"
    if not os.path.exists(szMainFilePath):
        print("current working dir is not right")
        raise FileNotFoundError(szMainFilePath)


def InitLog():
    # 初始化log配置
    if not os.path.exists("log"):  # 不存在log目录，要创建
        os.makedirs("log")

    szLogConfPath = os.getcwd() + "/config/log.conf"
    if not os.path.exists(szLogConfPath):
        raise FileNotFoundError(szLogConfPath)

    logging.config.fileConfig(os.getcwd() + "/config/log.conf")


def InitSysPath():
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd() + "/lib")
    sys.path.append(os.getcwd() + "/unit_test")
    logging.getLogger("myLog").info("sys path:" + str(sys.path))


def StartUnitTest():
    logging.getLogger("myLog").info("start unit test:\n\n\n")
    szTestDir = "./unit_test"
    discover = unittest.defaultTestLoader.discover(szTestDir, pattern="test*.py", top_level_dir="")
    runner = unittest.TextTestRunner()
    TestResultObj = runner.run(discover)

    logging.getLogger("myLog").info("unit test result:" + str(TestResultObj))
    if not TestResultObj.wasSuccessful():
        import common.my_exception as my_exception
        # print("unit test failed, result:" + "".join(TestResultObj.failures(),"\n"))
        raise my_exception.MyException("unit test failed")


def Main(args):
    # 检查当前目录
    CheckCWD()

    # 初始化log
    InitLog()

    # 初始化路径
    InitSysPath()

    # app初始化
    import logic.main_app as main_app
    AppCls = main_app.GetAppCls()
    builtins.g_AppObj = AppCls()
    g_AppObj.DoInit(args)

    # 开始执行单元测试
    StartUnitTest()

    # app销毁
    g_AppObj.Destroy()


if __name__ == '__main__':
    print(Main(sys.argv))
