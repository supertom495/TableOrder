import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import common
import logging



# logTest()
def setLogger():  
    # 创建一个logger,可以考虑如何将它封装  
    logger = logging.getLogger('mylogger')  
    logger.setLevel(logging.DEBUG)  

    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler(os.path.join(os.getcwd(), './API_data/log.txt'))  
    fh.setLevel(logging.DEBUG)  

    # 再创建一个handler，用于输出到控制台  
    ch = logging.StreamHandler()  
    ch.setLevel(logging.DEBUG)  

    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  

    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)  

    # 记录一条日志  
    logger.info('hello world, i\'m log helper in python, may i help you')  
    return logger


# common.setUpWebsocketServer()
def logTest():
    logger = setLogger()
    try:
        name = []
        aa = name[0]
    except:
        logger.exception("Exception Logged")


logTest()
