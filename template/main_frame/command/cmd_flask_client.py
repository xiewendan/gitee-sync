# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 22:23

# desc: 上传文件示例

if __name__ == '__main__':
    import os
    import requests
    import common.stat_mgr as stat_mgr

    # szUrl = "http://10.249.80.162:5000/upload"
    # szUrl = "http://10.212.32.132:5000/upload"
    szUrl = "http://127.0.0.1:5000/upload"
    szPath = os.getcwd() + "/data/local/test1G.7z"

    StatMgrObj = stat_mgr.StatMgr()
    StatMgrObj.LogTimeTag("begin")

    dictFile = {'file': open(szPath, 'rb')}

    RequestObj = requests.post(szUrl, files=dictFile)

    print(RequestObj.url)
    print(RequestObj.text)

    StatMgrObj.LogTimeTag("end")
    print(StatMgrObj.GetTimeTagStat())
