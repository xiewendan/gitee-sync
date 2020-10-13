import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json  # 导入依赖库
import logging

g_szKeyWord = "xiaoxiao"
g_szSecret = "SEC3ec7794df9406701df3307b96877e8868f7bb883e442ad15b66032e5d0218d11"
# 定义webhook，从钉钉群机器人设置页面复制获得
g_szWebhook = 'https://oapi.dingtalk.com/robot/send?access_token=e5dbbb8cc5a8206dba1b8d16c9b6691224e9afc71b959aa688df081b3242f72e'


class DingDingMgr:
    def __init__(self, szWebhook, szSecret, szKeyword, listTo):
        logging.getLogger("myLog").info(
            "init dingding mgr, webhook:%s, secret:%s, keyword:%s, listTo:%s", szWebhook, szSecret, szKeyword, ",".join(listTo))
        self.m_szWebhook = szWebhook
        self.m_szSecret = szSecret
        self.m_szKeyword = szKeyword

        assert self._CheckListTo(listTo), "目标列表有问题"
        self.m_listTo = listTo

    def Send(self, szMsg, listTargetMobile=None):
        logging.getLogger("myLog").info("msg:%s, listTo:%s", szMsg, repr(listTargetMobile))

        if len(szMsg) == 0:
            logging.getLogger("myLog").info("send msg is empty")
            return

        if listTargetMobile is None:
            listTargetMobile = self.m_listTo

        if not self._CheckListTo(listTargetMobile):
            return

        szTimeStamp, szSign = self._GetTimeStampSign()
        szWebhook = "%s&timestamp=%s&sign=%s" % (
            self.m_szWebhook, szTimeStamp, szSign)

        # 定义要发送的数据
        dictData = {
            "msgtype": "text",
            "text": {
                "content": "@%s\n%s\n%s" % ("@".join(listTargetMobile), szMsg, self.m_szKeyword)
            },
            "at": {
                "atMobiles": listTargetMobile,
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

        requests.post(szWebhook, data=json.dumps(dictData),
                                headers=dictHeaders)  # 发送post请求

        # if dictRet.errcode == 310000:
        #     raise dictRet.errmsg

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
