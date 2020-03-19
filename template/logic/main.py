# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import sys
import logging
import common.util as util
import common.command_line_arg_mgr as command_line_arg_mgr


def Main(args):
    logging.getLogger("myLog").debug("main start")

    # command line
    commandLineArgMgr = command_line_arg_mgr.CommandLineArgMgr("hc:", ["help", "config="])
    commandLineArgMgr.Parse(args)
    szConf = commandLineArgMgr.GetOpt("-c", "-config")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(szConf)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()


    # todo

    logging.getLogger("myLog").debug("finished")

