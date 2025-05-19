import logging

def setup_logger(name, level=logging.INFO, log_file=None):
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 清除已有处理器
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    # 创建控制台处理器
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    # 创建文件处理器（如果指定了日志文件）
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        logger.addHandler(fh)
    
    # 创建格式化器并添加到处理器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    if log_file:
        fh.setFormatter(formatter)
    
    # 添加处理器到logger
    logger.addHandler(ch)
    
    return logger    