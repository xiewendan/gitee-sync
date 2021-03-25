# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/5 18:55

# desc: 

import hashlib
import os

FILE_READ_LEN = 1024


def GetFileMD5(szFullPath):
    assert os.path.exists(szFullPath), "传入的路径不存在:{}".format(szFullPath)

    Md5Obj = hashlib.md5()
    with open(szFullPath, "rb") as FileObj:
        while True:
            szData = FileObj.read(FILE_READ_LEN)
            if szData == b'':
                break
            Md5Obj.update(szData)

    return Md5Obj.hexdigest()


def GetStrMD5(szData):
    Md5Obj = hashlib.md5()
    Md5Obj.update(szData.encode("utf-8"))

    return Md5Obj.hexdigest()


if __name__ == '__main__':
    # szPath = "E:/project/xiewendan/tools/template/unit_test/test_data/file_cache_system/1.data"
    szPath = "E:/project/xiewendan/tools/template/unit_test/test_data/file_cache_system/trunk__c74dcf98c_u74dcf98c.ipa"
    szMD5 = GetFileMD5(szPath)
    print(szMD5)
    print(len(szMD5))

    print(os.path.getsize(szPath))
