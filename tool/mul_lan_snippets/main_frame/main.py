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
        raise Exception("current working dir is not right:" + os.getcwd())


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

    szLibPath = os.getcwd() + "/lib"
    if not os.path.exists(szLibPath):
        raise FileNotFoundError(szLibPath)

    sys.path.append(szLibPath)
    logging.getLogger("myLog").debug("add sys path:" + szLibPath)


def StartApp(args):
    logging.getLogger("myLog").info("Start app")
    import logic.main_app as main_app
    AppCls = main_app.GetAppCls()
    AppObj = AppCls()
    AppObj.DoInit(args)
    AppObj.DoLogic()
    AppObj.Destroy()


def Main(args):
    print("Begin:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))

    # 检查当前目录是否正常
    CheckCWD()

    # 初始化log配置
    InitLog()

    # 初始化python 路径
    InitSysPath()

    # start app
    try:
        StartApp(args)
    except Exception as e:
        import traceback
        logging.getLogger("myLog").error("\n\n{0}\n".format(traceback.format_exc()))
        raise

    print("End:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == "__main__":
    Main(sys.argv)

