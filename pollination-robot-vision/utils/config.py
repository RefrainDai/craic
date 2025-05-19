class Config:
    """系统配置参数"""
    
    # 摄像头配置
    CAMERA_ID = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    
    # 花朵检测配置
    MIN_FLOWER_AREA = 500
    MAX_FLOWER_AREA = 5000
    FEMALE_YELLOW_RATIO = 0.3  # 雌花黄色区域比例阈值
    
    # 授粉验证配置
    MIN_SUCCESSFUL_POLLINATION_PIXELS = 50  # 最小成功授粉像素数
    
    # 障碍物检测配置
    MIN_OBSTACLE_AREA = 1000  # 最小障碍物面积
    
    # 授粉点定位配置
    POLLINATION_OFFSET_X = 0  # 授粉点X偏移
    POLLINATION_OFFSET_Y = 0  # 授粉点Y偏移
    
    # 调试模式
    DEBUG = True    