# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 09:29:16

# desc: 主流程

import builtins
import logging
import logging.config
import os
import socket
import sys
import time

g_MaxStrLen = 2000


def Str(DataObj):
    return str(DataObj)[:500]


def CheckCWD():
    print(os.getcwd())
    szMainFilePath = os.getcwd() + "/main_frame/main.py"
    if not os.path.exists(szMainFilePath):
        raise Exception("current working dir is not right:" + os.getcwd())


def InitLog():
    # 初始化log配置
    if not os.path.exists("log"):  # 不存在log目录，要创建
        os.makedirs("log")

    import colorlog
    colorlog.getLogger('myLog').setLevel(logging.DEBUG)
    colorlog.getLogger("root").setLevel(logging.DEBUG)

    # 控制台log
    ConsoleHandlerObj = colorlog.StreamHandler()
    ConsoleFormatterObj = colorlog.ColoredFormatter("%(log_color)s%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d  %(funcName)s] - %(message)s")
    ConsoleHandlerObj.setFormatter(ConsoleFormatterObj)
    ConsoleHandlerObj.setLevel(logging.INFO)

    colorlog.getLogger("myLog").addHandler(ConsoleHandlerObj)
    colorlog.getLogger("root").addHandler(ConsoleHandlerObj)

    # 文件log
    import datetime
    szTime = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S.%f")
    szLogFileName = "log/{0} {1}.log".format(socket.gethostname(), szTime)

    FileHandlerObj = logging.FileHandler(szLogFileName)
    FileFormatterObj = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d  %(funcName)s] - %(message)s')
    FileHandlerObj.setFormatter(FileFormatterObj)

    logging.getLogger("myLog").addHandler(FileHandlerObj)
    logging.getLogger("root").addHandler(FileHandlerObj)

    logging.getLogger("myLog").info("Init log!")


def InitTraceback():
    import common.my_trackback as my_traceback
    my_traceback.Init()


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
    builtins.g_AppObj = AppObj

    logging.getLogger("myLog").info("Do init app")
    AppObj.DoInit(args)

    logging.getLogger("myLog").info("App run")
    AppObj.DoLogic()

    logging.getLogger("myLog").info("Destroy app")
    AppObj.Destroy()


def Main(args):
    print(args)
    print("Begin:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))

    builtins.Str = Str

    # 检查当前目录是否正常
    CheckCWD()

    # 初始化log配置
    InitLog()

    # 初始化python 路径
    InitSysPath()

    # 初始化异常处理
    InitTraceback()

    # start app
    StartApp(args)

    print("End:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == "__main__":
    Main(sys.argv)
