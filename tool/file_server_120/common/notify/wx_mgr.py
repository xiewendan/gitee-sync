# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/1 9:55 下午

# desc: 微信管理器
# 不建议高频使用，可能会被封号

import itchat


class WXMgr:
    def __init__(self):
        self.m_bLogin = False

    def Send(self, szMsg, szName=None):
        """不建议高频调用，会被封号"""

        if not self.m_bLogin:
            itchat.auto_login(hotReload=True)
            self.m_bLogin = True

        if szName is None:
            szName = "filehelper"
            itchat.send(szMsg, szName)
        else:
            listUser = itchat.search_friends(szName)
            szUserName = listUser[0]['UserName']
            itchat.send(szMsg, toUserName=szUserName)
