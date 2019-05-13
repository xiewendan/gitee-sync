# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/5/14 下午12:49

# desc: 清理磁盘空间
import os
import shutil
import stat
import subprocess


class ClearWinMgr(object):
    def __init__(self):
        pass

    def clear_all(self):
        self.clear_app_data()

    @staticmethod
    def clear_app_data():
        listDirDel = [
            r"C:/Users/gzxiejinchun/AppData/Roaming/Listary/UserData",
            r"C:/Users/gzxiejinchun/Documents/MuMu共享文件夹",
            r"C:/Users/gzxiejinchun/Documents/NVIDIA Nsight/Captures",
            r"C:/Users/gzxiejinchun/AppData/Local/CrashDumps",
            r"C:/Users/gzxiejinchun/AppData/Roaming/Unity",
        ]

        import shutil
        for szDir in listDirDel:
            if os.path.exists(szDir):
                shutil.rmtree(szDir)

    @staticmethod
    def RunCmd(szCmd):
        print( "RunCmd:", szCmd )

        p = subprocess.Popen(szCmd, shell=True)

        return p.wait()


def main():
    clear_windows_mgr_obj = ClearWinMgr()
    clear_windows_mgr_obj.clear_all()


if __name__ == '__main__':
    main()
