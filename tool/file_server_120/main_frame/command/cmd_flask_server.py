# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 12:21

# desc: flask的server服务器

import os

from flask import Flask, request
from werkzeug.utils import secure_filename

import main_frame.cmd_base as cmd_base
import common.my_path as my_path
import common.my_log as my_log

g_FlaskApp = Flask(__name__)
g_LoggerObj = None


class CmdFlaskServer(cmd_base.CmdBase):
    def __init__(self):
        super(CmdFlaskServer, self).__init__()

        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetName():
        return "flask_server"

    def Do(self):
        self.m_LoggerObj.info("Start do %s", self.GetName())

        szCWD = self.m_AppObj.ConfigLoader.CWD
        szHost = self.m_AppObj.CLM.GetArg(1)
        szPort = self.m_AppObj.CLM.GetArg(2)

        g_FlaskApp.run(debug=True, host=szHost, port=szPort)


def _GetLoggerObj():
    global g_LoggerObj
    if g_LoggerObj is None:
        g_LoggerObj = my_log.MyLog(__file__)

    return g_LoggerObj


@g_FlaskApp.route("/upload", methods=['POST'])
def Upload():
    FileObj = request.files['file']
    _GetLoggerObj().info("upload file name:%s", secure_filename(FileObj.filename))

    szCWD = os.getcwd()
    szUploadFileFullPath = os.path.join(szCWD, 'data/uploads', secure_filename(FileObj.filename))
    my_path.CreateFileDir(szUploadFileFullPath)

    FileObj.save(szUploadFileFullPath)

    OnHandleUploadFile(szUploadFileFullPath)

    return "succeed"


def OnHandleUploadFile(szUploadFileFullPath):
    _GetLoggerObj().info("handle file name:%s", szUploadFileFullPath)
