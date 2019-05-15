# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 14:43

# desc: 自己的配置文件加载器

import logging
import main_frame.config_loader as config_loader


class MyConfigLoader(config_loader.ConfigLoader):
    """"""
    
    def __init__(self, szConfFullPath):
        super(MyConfigLoader, self).__init__(szConfFullPath)

        self.m_szVSCodeWorkspacePath = None
        self.m_szExtList = None
        self.m_szExcludeList = None

    def ParseConf(self):
        self.m_szVSCodeWorkspacePath = self.ParseStr("common", "VSCodeWorkspacePath")
        logging.getLogger("myLog").info("VSCodeWorkspacePath:" + self.m_szVSCodeWorkspacePath)

        self.m_szExtList = self.ParseStr("common", "ExtList")
        logging.getLogger("myLog").info("ExtList:" + self.m_szExtList)

        self.m_szExcludeList = self.ParseStr("common", "ExcludeList")
        logging.getLogger("myLog").info("ExcludeList:" + self.m_szExcludeList)

        return True

    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def VSCodeWorkspacePath(self):
        return self.m_szVSCodeWorkspacePath

    @property
    def ExtList(self):
        return self.m_szExtList

    @property
    def ExcludeList(self):
        return self.m_szExcludeList
