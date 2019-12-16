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

        self.m_szTest = None
        self.m_szTrunk = None
        self.m_szSvnIgnoreJson = None

    def ParseConf(self):
        self.m_szTrunk = self.ParseStr("common", "trunk")
        self.m_szSvnIgnoreJson = self.ParseStr("common", "svnignorejson")
        return True

    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def Test(self):
        return self.m_szTest

    @property
    def Trunk(self):
        return self.m_szTrunk


    @property
    def SvnIgnoreJson(self):
        return self.m_szSvnIgnoreJson
