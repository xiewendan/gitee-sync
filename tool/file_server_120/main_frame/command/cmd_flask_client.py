# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 22:23

# desc: 上传文件示例

import common.stat_mgr as stat_mgr

if __name__ == '__main__':
    import os
    import requests

    # szUrl = "http://10.249.80.162:5000/upload"
    szUrl = "http://10.249.81.105:5000/upload"
    # szUrl = "http://10.249.81.85:5000/upload"
    # szPath = os.getcwd() + "/data/local/1.txt"
    szPath = os.getcwd() + "/data/local/test1G.7z"
    print(szPath)

    StatMgrObj = stat_mgr.StatMgr()
    StatMgrObj.LogTimeTag("start")

    dictFile = {'file': open(szPath, 'rb')}

    RequestObj = requests.post(szUrl, files=dictFile)

    print(RequestObj)
    StatMgrObj.LogTimeTag("end")
    print(StatMgrObj.GetTimeTagStat())
