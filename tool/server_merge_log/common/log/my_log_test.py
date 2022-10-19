# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/12/10 上午9:06

# desc: 自己的log,log初始化
# 使用说明:
# 1 配置conf文件
# 2 初始化
#   import logging
#   import logging.config
#   logging.config.fileConfig("log.conf")
#   logger = logging.getLogger("packageLog")
# 3 调用记录log
#   logger.debug("debug")
#   logger.info("info")
#   logger.warn("warn")
#   logger.error("error")
#   logger.critical("critical")



if __name__ == '__main__':
    import logging
    import logging.config

    # 读取日志配置文件内容
    logging.config.fileConfig("log.conf")

    # 创建一个日志器logger
    logger = logging.getLogger("packageLog")

    # 日志输出
    logger.debug("debug")
    logger.info("info")
    logger.warn("warn")
    logger.error("error")
    logger.critical("critical")
