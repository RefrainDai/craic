from .config import Config

class CompetitionConfig(Config):
    """比赛环境配置 - 覆盖基础配置"""
    DEBUG_MODE = False
    LOG_LEVEL = "WARNING"
    MOTOR_SPEED = 70        # 比赛时提高速度
    APPROACH_SPEED = 40    