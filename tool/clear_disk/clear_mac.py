# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/5/14 下午12:49

# desc: 清理磁盘空间


class ClearMacMgr(object):
    def __init__(self):
        pass

    def clear_all(self):
        self.clear_xcode()

    @staticmethod
    def clear_xcode():
        import os
        import shutil
        shutil.rmtree(r"/Users/stephenxjc/Library/Developer/Xcode/iOS DeviceSupport")
        os.mkdir(r"/Users/stephenxjc/Library/Developer/Xcode/iOS DeviceSupport")


def main():
    clear_mac_mgr_obj = ClearMacMgr()
    clear_mac_mgr_obj.clear_all()


if __name__ == '__main__':
    main()
