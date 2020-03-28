# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 09:29:16

# desc: 主流程

import logging
import logging.config
import os
import sys
import time


def CheckCWD():
    print(os.getcwd())
    szMainFilePath = os.getcwd() + "/main_frame/main.py"
    if not os.path.exists(szMainFilePath):
        print("current working dir is not right")
        raise FileNotFoundError(szMainFilePath)


def InitSysPath():
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd() + "/lib")
    logging.getLogger("myLog").debug("add sys path:" + os.getcwd() + "/lib")


def InitLog():
    # 初始化log配置
    if not os.path.exists("log"):  # 不存在log目录，要创建
        os.makedirs("log")

    szLogConfPath = os.getcwd() + "/conf/log.conf"
    if not os.path.exists(szLogConfPath):
        raise FileNotFoundError(szLogConfPath)

    logging.config.fileConfig(os.getcwd() + "/conf/log.conf")


def StartApp(args):
    import logic.main_app as main_app
    AppCls = main_app.GetAppCls()
    AppObj = AppCls()
    AppObj.DoInit(args)
    AppObj.DoLogic()


def Main(args):
    print("Begin:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))

    # 检查当前目录是否正常
    CheckCWD()

    # 初始化log配置
    InitLog()

    # 初始化python 路径
    InitSysPath()

    # start app
    StartApp(args)

    print("End:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == "__main__":
    Main(sys.argv)
