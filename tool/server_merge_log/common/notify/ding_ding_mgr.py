import base64
import hashlib
import hmac
import json  # 导入依赖库
import logging
import time
import urllib.parse

import requests

import common.my_exception as my_exception


class DingDingMgr:
    def __init__(self, szWebhook, szSecret, szKeyword, listTo):
        logging.getLogger("myLog").info(
            "init dingding mgr, webhook:%s, secret:%s, keyword:%s, listTo:%s", szWebhook, szSecret, szKeyword, ",".join(listTo))
        self.m_szWebhook = szWebhook
        self.m_szSecret = szSecret
        self.m_szKeyword = szKeyword

        assert self._CheckListTo(listTo), "目标列表有问题"
        self.m_listTo = listTo

    def Send(self, szMsg, listTo=None):
        logging.getLogger("myLog").info(
            "msg:%s, listTo:%s", szMsg, repr(listTo))

        if len(szMsg) == 0:
            logging.getLogger("myLog").info("send msg is empty")
            return

        if listTo is None:
            listTo = self.m_listTo

        if not self._CheckListTo(listTo):
            return

        szTimeStamp, szSign = self._GetTimeStampSign()
        szWebhook = "%s&timestamp=%s&sign=%s" % (
            self.m_szWebhook, szTimeStamp, szSign)

        # 定义要发送的数据
        dictData = {
            "msgtype": "text",
            "text": {
                "content": "@%s\n%s\n%s" % ("@".join(listTo), szMsg, self.m_szKeyword)
            },
            "at": {
                "atMobiles": listTo,
                "isAtAll": False
            }
        }

        dictHeaders = {'Content-Type': 'application/json'}  # 定义数据类型

        # // 消息内容中不包含任何关键词
        # {
        #   "errcode": 310000,
        #   "errmsg": "keywords not in content"
        # }

        # // timestamp 无效
        # {
        #   "errcode": 310000,
        #   "errmsg": "invalid timestamp"
        # }

        # // 签名不匹配
        # {
        #   "errcode": 310000,
        #   "errmsg": "sign not match"
        # }

        # // IP地址不在白名单
        # {
        #   "errcode": 310000,
        #   "errmsg": "ip X.X.X.X not in whitelist"
        # }

        logging.getLogger("myLog").info(
            "dingding post\n webhook:%s,\n data:%s,\n headers:%s", szWebhook, repr(dictData), repr(dictHeaders))
        ResponseObj = requests.post(szWebhook, data=json.dumps(dictData),
                                    headers=dictHeaders)  # 发送post请求
        logging.getLogger("myLog").info(
            "dingding post webhook ret:\n%s",
            '\n'.join(['%s:%s' % item for item in ResponseObj.__dict__.items()])
        )

        dictRet = json.loads(ResponseObj._content)
        if dictRet["errcode"] == 310000:
            raise my_exception.MyException(dictRet["errmsg"])

    def _GetTimeStampSign(self):
        szTimeStamp = str(round(time.time() * 1000))
        szSecretEnc = self.m_szSecret.encode('utf-8')
        szSecretToSign = '{}\n{}'.format(szTimeStamp, self.m_szSecret)
        szSecretToSignEnc = szSecretToSign.encode('utf-8')
        HmacCodeObj = hmac.new(
            szSecretEnc, szSecretToSignEnc, digestmod=hashlib.sha256).digest()
        szSign = urllib.parse.quote_plus(base64.b64encode(HmacCodeObj))

        return szTimeStamp, szSign

    def Destroy(self):
        pass

    def _CheckListTo(self, listTo):
        if listTo is None:
            logging.getLogger("myLog").info(
                "send msg target mobile error: list is None")
            return False

        if len(listTo) == 0:
            logging.getLogger("myLog").info(
                "send msg target mobile error: list is empty")
            return False

        for szTo in listTo:
            if not isinstance(szTo, str):
                logging.getLogger("myLog").info(
                    "send msg target mobile error: not all mobile is str")
                return False

        return True
