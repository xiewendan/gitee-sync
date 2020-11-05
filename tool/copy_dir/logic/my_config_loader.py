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
        self.m_szCpConfig = None

    def ParseConf(self):
        self.m_szCpConfig = self.ParseStr("common", "cp_config")
        return True

    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def Test(self):
        return self.m_szTest

    @property
    def CpConfig(self):
        return self.m_szCpConfig

