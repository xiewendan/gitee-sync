# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import sys
import logging
import common.util as util
import common.svn_util as svn_util
import json


def Main(args):
    logging.getLogger("myLog").debug("main start")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(args)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()

    # test render
    # dictTemplatePath2TargetPath = {}
    # dictTemplatePath2TargetPath["test/render/1.txt"] = "test/render/2.txt"
    # util.RenderConfig("conf/render_template.yml", dictTemplatePath2TargetPath)

    
    trunk = configLoader.Trunk
    with open(configLoader.SvnIgnoreJson, "r") as load_f:
        load_dict = json.load(load_f)
        for szKey, listValue in load_dict.items():
            with open("conf/svnignore.txt", 'w') as fp:
                for szValue in listValue:
                    fp.write(szValue)
                    fp.write("\n")
            
            svn_util.SvnUtil.SvnIgnoreByCfgFile(trunk + "/" + szKey, "conf/svnignore.txt")

    # todo

    logging.getLogger("myLog").debug("finished")

