# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/2 10:07 上午

# desc:

import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import email.utils as email_utils


class MailMgr:
    def __init__(self):
        self.m_smtpObj = None

    def Login(self, szMailHost, szMailUser, szMailPassword):
        logging.getLogger("myLog").info("Start login:%s, %s", szMailHost, szMailUser)
        self.m_smtpObj = smtplib.SMTP()

        nCode, szError = self.m_smtpObj.connect(szMailHost, 25)
        if nCode == -1:
            logging.getLogger("myLog").error(szError)
            raise
        else:
            logging.getLogger("myLog").info("Connect %s succeed", szMailHost)

        self.m_smtpObj.login(szMailUser, szMailPassword)
        logging.getLogger("myLog").info("Login succeed: %s", szMailUser)

    def Send(self, szFrom, listTo, szTitle, szMsg):
        print(szFrom, listTo, szTitle, szMsg)
        logging.getLogger("myLog").info("Send mail! From: %s, To: %s, szTitle: %s, szMsg: %s", szFrom, listTo,
                                        szTitle, szMsg)

        if len(listTo) == 0:
            logging.getLogger("myLog").error("Send mail failed: no receiver")
            return

        assert self.m_smtpObj is not None, "You did not login success, try call Login"

        MTextObj = MIMEText(szMsg, 'plain', 'utf-8')
        MTextObj['From'] = szFrom
        MTextObj['To'] = ",".join(listTo)
        MTextObj['Subject'] = Header(szTitle, 'utf-8')

        listToError = self.m_smtpObj.sendmail(szFrom, listTo, MTextObj.as_string())
        if len(listToError) > 0:
            logging.getLogger("myLog").error("Send mail failed list: %s", listToError)

    def Destroy(self):
        logging.getLogger("myLog").info("Destroy mail obj")
        self.m_smtpObj.quit()

