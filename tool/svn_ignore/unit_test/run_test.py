# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/08/08 12:30:42

# desc: desc

import os
import sys
import unittest
import logging
import logging.config

def InitLog():
    # 初始化log配置
    if not os.path.exists("log"):       # 不存在log目录，要创建
        os.makedirs("log")
    logging.config.fileConfig(os.getcwd() + "/conf/log.conf")

def InitSysPath():
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd() + "/lib")
    sys.path.append(os.getcwd() + "/unit_test")
    logging.getLogger("myLog").info("sys path:" + str(sys.path))
    
def Main():
    # 初始化log
    InitLog()

    # 初始化路径
    InitSysPath()

    szTestDir = "./unit_test"
    discover = unittest.defaultTestLoader.discover(szTestDir, pattern="test*.py", top_level_dir="")
    runner = unittest.TextTestRunner()
    TestResultObj = runner.run(discover)


    logging.getLogger("myLog").info("unit test result:" + str(TestResultObj))
    if not TestResultObj.wasSuccessful():
        import common.my_exception as my_exception
        # print("unit test failed, result:" + "".join(TestResultObj.failures(),"\n"))
        raise my_exception.MyException("unit test failed")

if __name__ == '__main__':
    print(Main())