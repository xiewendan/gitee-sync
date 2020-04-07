# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/12/09 15:35:55

# desc: 配置表加载器
# 需要自定义加载器，可以继承于ConfigLoader


import configparser
import logging
import os

import common.my_exception as my_exception

ARGS_NUM = 1


class ConfigLoader(object):
    def __init__(self, szConfFullPath):
        logging.getLogger("myLog").debug("ConfigLoader.__init__:" + szConfFullPath)

        self.m_szCWD = os.getcwd()

        self.m_szConfFullPath = szConfFullPath
        self.m_configParser = self.CreateConfigParser(self.m_szConfFullPath)

        self.m_szConfTempFullPath = self.m_szCWD + "/conf/conf_template.conf"
        self.m_tempConfigParser = self.CreateConfigParser(self.m_szConfTempFullPath)

        # 定义的配置
        self.m_szName = "default"

        # mail
        self.m_szMailUser = None
        self.m_szMailPassword = None
        self.m_szMailHost = None

    def ReplaceCWD(self, szStr):
        return szStr.replace("%cwd%", self.m_szCWD)

    @staticmethod
    def CreateConfigParser(szConfFullPath):
        logging.getLogger("myLog").debug("ConfigLoader.ParseConf:" + szConfFullPath)

        if not os.path.exists(szConfFullPath):
            raise my_exception.MyException("Conf file not exits:%s" % szConfFullPath)

        configParser = configparser.ConfigParser()
        try:
            configParser.read(szConfFullPath)
        except Exception:
            logging.getLogger("myLog").error("Create config parser failed!%s" % szConfFullPath)
            raise

        return configParser

    def ParseStr(self, szSection, szKey):
        try:
            return self.m_configParser.get(szSection, szKey)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.m_tempConfigParser.get(szSection, szKey)

    def ParseBool(self, szSection, szKey):
        try:
            return self.m_configParser.getboolean(szSection, szKey)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return self.m_tempConfigParser.getboolean(szSection, szKey)

    def ParseConf(self):
        self.m_szMailHost = self.ParseStr("mail", "host")
        self.m_szMailUser = self.ParseStr("mail", "user")
        self.m_szMailPassword = self.ParseStr("mail", "password")

        return True

    @staticmethod
    def CheckConf(szConfPath=None):
        if szConfPath is None:
            szConfName = "conf/conf.conf"
            logging.getLogger("myLog").debug("use default conf:conf.conf")
        else:
            szConfName = szConfPath
            logging.getLogger("myLog").debug("Use define conf:%s", szConfName)

        szConfFullPath = os.getcwd() + "/" + szConfName
        if not os.path.exists(szConfFullPath):
            raise my_exception.MyException("Conf file not exits:%s" % szConfFullPath)

        return szConfFullPath

    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def Name(self):
        return self.m_szName

    @property
    def MailHost(self):
        return self.m_szMailHost

    @property
    def MailUser(self):
        return self.m_szMailUser

    @property
    def MailPassword(self):
        return self.m_szMailPassword
