# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/12/09 15:35:55

# desc: 配置表加载器
# 需要自定义加载器，可以继承于ConfigLoader


import os
import logging
import configparser
import common.my_exception as my_exception

ARGS_NUM = 2


class ConfigLoader(object):
    def __init__(self, szConfFullPath):
        logging.getLogger("myLog").debug("ConfigLoader.__init__:" + szConfFullPath)

        self.m_szConfFullPath = szConfFullPath
        self.m_szCWD = os.getcwd()
        self.m_szConfTempFullPath = self.m_szCWD + "/conf/conf_template.conf"
        self.m_configParser = self.CreateConfigParser(self.m_szConfFullPath)
        self.m_tempConfigParser = self.CreateConfigParser(self.m_szConfTempFullPath)

        self.m_szName = "default"

    def ReplaceCWD(self, szStr):
        return szStr.replace("%cwd%", self.m_szCWD)

    def CreateConfigParser(self, szConfFullPath):
        if not os.path.exists(szConfFullPath):
            raise my_exception.MyException(
                "Conf file not exits:%s" % szConfFullPath)

        logging.getLogger("myLog").debug("ConfigLoader.ParseConf:" + szConfFullPath)

        configParser = configparser.ConfigParser()
        try:
            configParser.read(szConfFullPath)
        except Exception as e:
            logging.getLogger("myLog").debug(e.message)
            logging.getLogger("myLog").debug("Config parser failed:%s" % szConfFullPath)
            raise my_exception.MyException("create config parser failed!")

        return configParser

    def ParseStr(self, szSection, szKey):
        try:
            return self.m_configParser.get(szSection, szKey)
        except Exception as e:
            return self.m_tempConfigParser.get(szSection, szKey)

    def ParseBool(self, szSection, szKey):
        try:
            return self.m_configParser.getboolean(szSection, szKey)
        except Exception as e:
            return self.m_tempConfigParser.getboolean(szSection, szKey)

    def ParseConf(self):
        return True

    @staticmethod
    def CheckConf(args):
        import common.my_exception as my_exception

        if len(args) == 1:
            szConfName = "conf/conf.conf"
            logging.getLogger("myLog").debug("use default conf:conf.conf")
        elif len(args) == ARGS_NUM:
            szConfName = args[1]
            logging.getLogger("myLog").debug("Use define conf:%s", szConfName)
        else:
            raise my_exception.MyException(
                "[Error] Args num error! Need args num == %s. Give: %s" % (ARGS_NUM, len(args)))

        szConfFullPath = os.getcwd() + "/" + szConfName
        if not os.path.exists(szConfFullPath):
            raise my_exception.MyException(
                "Conf file not exits:%s" % szConfFullPath)

        return szConfFullPath


    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def Name(self):
        return self.m_szName
