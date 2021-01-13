# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 22:23

# desc: 上传文件示例

if __name__ == '__main__':
    import requests

    szUrl = "http://10.249.80.162:5000/upload"
    szPath = r"F:\bd_download\1.txt"

    dictFile = {'file': open(szPath, 'rb')}

    RequestObj = requests.post(szUrl, files=dictFile)

    print(RequestObj.url)
    print(RequestObj.text)
