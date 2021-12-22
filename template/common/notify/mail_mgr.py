# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/4/2 10:07 上午

# desc:

import json
import time
import logging
import queue
import smtplib
import threading
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

        self.m_queueObj = queue.Queue()

        # 销毁
        self.m_bDestroying = False
        self.m_DestroyingThreadLockObj = threading.Lock()

        # 发送线程
        self.m_SendingThreadObj = threading.Thread(target=self._Sending)
        self.m_SendingThreadObj.start()

    def Destroy(self):
        logging.getLogger("myLog").info("Destroy mail obj")

        self.m_DestroyingThreadLockObj.acquire()
        self.m_bDestroying = True
        self.m_DestroyingThreadLockObj.release()

        logging.getLogger("myLog").info("join sending mail thread")
        self.m_SendingThreadObj.join()
        logging.getLogger("myLog").info("join sending mail thread end")

        self.UnLogin()

    def UnLogin(self):
        logging.getLogger("myLog").info("unlogin")
        if self._CheckLogin():
            self.m_smtpObj.quit()
            self.m_smtpObj = None

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
        logging.getLogger("myLog").info(
            "Send mail add to queue! From: %s, To: %s, DefaultTo: %s, szTitle: %s, szMsg: %s",
            self.m_szMailUser,
            listTo,
            ",".join(self.m_listMailTo),
            szTitle,
            szMsg)

        self.m_DestroyingThreadLockObj.acquire()
        if self.m_bDestroying:
            logging.getLogger("myLog").error(
                "destroying, send failed, From: %s, To: %s, DefaultTo: %s, szTitle: %s, szMsg: %s",
                self.m_szMailUser,
                listTo,
                ",".join(self.m_listMailTo),
                szTitle,
                szMsg)
            self.m_DestroyingThreadLockObj.release()
            return

        self.m_queueObj.put((szTitle, szMsg, listTo))
        self.m_DestroyingThreadLockObj.release()

    def _Send(self, szTitle, szMsg, listTo=None):
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

    def _Sending(self):
        while True:
            # 锁
            self.m_DestroyingThreadLockObj.acquire()
            bEmpty = self.m_queueObj.empty()
            bDestroying = self.m_bDestroying
            self.m_DestroyingThreadLockObj.release()

            if bEmpty:
                if bDestroying:
                    logging.getLogger("myLog").info("sending mail thread close")
                    break
                else:
                    time.sleep(1)
            else:
                szTitle, szMsg, listTo = self.m_queueObj.get()
                self._Send(szTitle, szMsg, listTo)
                self.m_queueObj.task_done()
