# -*- coding: utf-8 -*-

# __author__ = stephenxjc@corp.netease.com
# __date__ = 2018/5/14 下午12:49

# desc: 清理磁盘空间
import os


class ClearWinMgr(object):
    def __init__(self):
        pass

    def clear_all(self):
        self.clear_app_data()

    @staticmethod
    def clear_app_data():
        import os
        import shutil
        listDirDel = [
            r"C:/Users/gzxiejinchun.GAME/AppData/Roaming/Listary/UserData",
            r"C:/Users/gzxiejinchun.GAME/AppData/LocalLow/Unity/Caches",
        ]

        for szDir in listDirDel:
            if os.path.exists(szDir):
                ClearWinMgr.del_dir(szDir)
            else:
                print("del dir failed, dir not exists:" + szDir)

    @staticmethod
    def del_dir(szDir):
        listSubDir = os.listdir(szDir)
        for szSubDir in listSubDir:
            szFullPath = os.path.join(szDir, szSubDir)
            if os.path.isfile(szFullPath):
                try:
                    os.remove(szFullPath)
                except Exception as e:
                    print("remove file failed:" + szFullPath)
            else:
                ClearWinMgr.del_dir(szFullPath)

        try:
            shutil.rmtree(szDir)
        except Exception as e:
            print("remove dir failed:" + szDir)


def main():
    clear_windows_mgr_obj = ClearWinMgr()
    clear_windows_mgr_obj.clear_all()


if __name__ == '__main__':
    main()
