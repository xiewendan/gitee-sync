# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 09:29:16

# desc: 主流程

import logging
import logging.config
import os
import sys
import time


def InitSysPath():
    sys.path.append(os.getcwd())
    sys.path.append(os.getcwd() + "/lib")
    logging.getLogger("myLog").debug("add sys path:" + os.getcwd() + "/lib")


def Main(args):
    print(os.getcwd())
    print("Begin:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))
    # 初始化log配置
    if not os.path.exists("log"):       # 不存在log目录，要创建
        os.makedirs("log")
    logging.config.fileConfig(os.getcwd() + "/conf/log.conf")

    # 初始化python 路径
    InitSysPath()

    import logic.main_app as main_app
    AppCls = main_app.GetAppCls()
    AppObj = AppCls()
    AppObj.DoInit(args)
    AppObj.DoLogic()

    print("End:\t" + time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == "__main__":
    Main(sys.argv)
