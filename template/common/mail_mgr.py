# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/2 10:07 上午

# desc:

import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import email.utils as email_utils


class MailMgr:
    def __init__(self):
        self.m_smtpObj = None

        self.m_szMailHost = None
        self.m_szMailUser = None
        self.m_szMailPassword = None
        self.m_listMailTo = None

    def SetDefaultConfig(self, szDefaultHost, szDefaultUser, szDefaultPassword, szDefaultTo):
        logging.getLogger("myLog").info("Host:%s, User:%s, To:%s", szDefaultHost, szDefaultUser, szDefaultTo)

        self.m_szMailHost = szDefaultHost
        self.m_szMailUser = szDefaultUser
        self.m_szMailPassword = szDefaultPassword
        self.m_listMailTo = szDefaultTo.split(",")

        assert len(self.m_listMailTo) > 0

    def _Login(self):
        self.m_smtpObj = smtplib.SMTP_SSL()
        nCode, szError = self.m_smtpObj.connect(self.m_szMailHost, 465)
        if nCode == -1:
            logging.getLogger("myLog").error(szError)
            raise
        else:
            logging.getLogger("myLog").info("Connect %s succeed", self.m_szMailHost)

        self.m_smtpObj.login(self.m_szMailUser, self.m_szMailPassword)
        logging.getLogger("myLog").info("Login succeed: %s", self.m_szMailUser)
    
    def _CheckLogin(self):
        if self.m_smtpObj is None:
            return False

        try:
            nStatus = self.m_smtpObj.noop()[0]
        except:
            nStatus = -1

        return nStatus == 250

    def Send(self, szTitle, szMsg, listTo=None):
        logging.getLogger("myLog").info("Send mail! From: %s, To: %s, DefaultTo: %s, szTitle: %s, szMsg: %s",
                                        self.m_szMailUser,
                                        listTo,
                                        ",".join(self.m_listMailTo),
                                        szTitle,
                                        szMsg)
        
        if listTo is None:
            listTo = self.m_listMailTo

        if len(listTo) == 0:
            logging.getLogger("myLog").error("Send mail failed: no receiver")
            return

        if not self._CheckLogin():
            self._Login()

        assert self.m_smtpObj is not None, "You did not login success, try call Login"

        MTextObj = MIMEText(szMsg, 'plain', 'utf-8')
        MTextObj['From'] = self.m_szMailUser
        MTextObj['To'] = ",".join(listTo)
        MTextObj['Subject'] = Header(szTitle, 'utf-8')

        listToError = self.m_smtpObj.sendmail(self.m_szMailUser, listTo, MTextObj.as_string())
        if len(listToError) > 0:
            logging.getLogger("myLog").error("Send mail failed list: %s", listToError)

    def Destroy(self):
        logging.getLogger("myLog").info("Destroy mail obj")
        if self._CheckLogin():
            self.m_smtpObj.quit()
