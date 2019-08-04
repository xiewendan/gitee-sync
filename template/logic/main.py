# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import sys
import logging
import common.util as util


def Main(args):
    logging.getLogger("myLog").debug("main start")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(args)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()

    # test render
    dictTemplatePath2TargetPath = {}
    dictTemplatePath2TargetPath["test/render/1.txt"] = "test/render/2.txt"
    util.RenderConfig("conf/render_template.yml", dictTemplatePath2TargetPath)

    # todo

    logging.getLogger("myLog").debug("finished")

