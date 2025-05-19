class Config:
    # 基础配置
    DEBUG_MODE = True
    LOG_LEVEL = "INFO"
    LOG_FILE = "robot.log"
    
    # 摄像头配置
    CAMERA_ID = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    FRAME_RATE = 30
    
    # 颜色识别阈值 (HSV)
    YELLOW_LOWER = (20, 100, 100)
    YELLOW_UPPER = (30, 255, 255)  # 雌花颜色
    WHITE_LOWER = (0, 0, 200)
    WHITE_UPPER = (180, 30, 255)   # 雄花/授粉标记颜色
    BLACK_LOWER = (0, 0, 0)
    BLACK_UPPER = (180, 255, 30)   # 障碍物颜色
    
    # 形态学操作参数
    ERODE_KERNEL = (5, 5)
    DILATE_KERNEL = (5, 5)
    ERODE_ITERATIONS = 1
    DILATE_ITERATIONS = 2
    
    # 花朵检测参数
    MIN_FLOWER_AREA = 500
    MAX_FLOWER_AREA = 5000
    
    # 运动控制参数
    MOTOR_SPEED = 50        # 前进速度
    TURN_SPEED = 30         # 转向速度
    APPROACH_SPEED = 30     # 接近花朵速度
    ROTATION_SPEED = 20     # 旋转速度
    BACKUP_SPEED = 40       # 后退速度
    APPROACH_DISTANCE = 15  # 接近花朵的距离 (厘米)
    POLLINATION_HEIGHT = 5  # 授粉高度 (厘米)
    
    # 比赛参数
    MAX_RUNNING_TIME = 600  # 最大运行时间 (秒)
    TOTAL_FEMALE_FLOWERS = 36  # 需要授粉的花朵总数    