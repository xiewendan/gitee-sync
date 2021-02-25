# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/25 19:57

# desc: service的模板


import common.my_log as my_log
import main_frame.service_base as service_base


class Template(service_base.ServiceBase):
    def __init__(self):
        super().__init__()
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetOptList():
        return ["-t", "--template"]

    @staticmethod
    def GetName():
        return "tempalte"

    def _GetDepServiceList(self):
        return []

    def _OnInit(self):
        self.m_LoggerObj.debug("_OnInit")

    def _OnDestroy(self):
        self.m_LoggerObj.debug("_OnDestroy")

