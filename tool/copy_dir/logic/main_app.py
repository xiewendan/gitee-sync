# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 3/22/2020 3:26 PM

# desc:

import os
import json
import re
import shutil
import logging
import main_frame.base_app as base_app
import common.my_path as my_path


def GetAppCls():
    return MainApp


class MainApp(base_app.BaseApp):
    @staticmethod
    def GetConfigLoaderCls():
        import logic.my_config_loader as my_config_loader
        return my_config_loader.MyConfigLoader

    def OnLogic(self):
        szCpConfig = self.GetConfigLoader().CpConfig
        logging.getLogger("myLog").debug("cp_config:%s", szCpConfig)

        with open(szCpConfig, "r") as fp:
            listCpConfig = json.load(fp)

        for dictData in listCpConfig:
            szFrom = dictData["from"].replace("\\", "/")
            szTo = dictData["to"].replace("\\", "/")
            listBlackList = dictData.get("blacklist_re","")
            szBlackList = "|".join(listBlackList)

            for root, dirs, files in os.walk(szFrom):
                for file in files:
                    szFromFullPath = os.path.join(root, file).replace("\\", "/")
                    # if not(szBlackList and re.match(szBlackList, szFromFullPath)):
                    szToFullPath = szFromFullPath.replace(szFrom, szTo)
                    my_path.CreateFileDir(szToFullPath)
                    logging.getLogger("myLog").debug("copy file:%s, %s", szFromFullPath, szToFullPath)
                    shutil.copyfile(szFromFullPath, szToFullPath)



