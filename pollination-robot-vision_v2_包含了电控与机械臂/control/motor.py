import time

class MotorController:
    """控制机器人的电机和移动"""
    
    def __init__(self, config):
        self.config = config
        # 初始化GPIO或电机驱动
        print("电机控制器初始化完成")
        
    def forward(self, speed=None):
        """向前移动"""
        speed = speed or self.config.MOTOR_SPEED
        print(f"电机向前，速度: {speed}")
        # 实际项目中这里会控制电机
        
    def backward(self, speed=None, duration=None):
        """向后移动"""
        speed = speed or self.config.BACKUP_SPEED
        print(f"电机向后，速度: {speed}")
        # 实际项目中这里会控制电机
        
        if duration:
            time.sleep(duration)
            self.stop()
        
    def turn_left(self, speed=None):
        """向左转"""
        speed = speed or self.config.TURN_SPEED
        print(f"电机左转，速度: {speed}")
        # 实际项目中这里会控制电机
        
    def turn_right(self, speed=None):
        """向右转"""
        speed = speed or self.config.TURN_SPEED
        print(f"电机右转，速度: {speed}")
        # 实际项目中这里会控制电机
        
    def rotate(self, speed=None, duration=0.5):
        """旋转"""
        speed = speed or self.config.ROTATION_SPEED
        print(f"电机旋转，速度: {speed}")
        # 实际项目中这里会控制电机
        
        time.sleep(duration)
        self.stop()
        
    def set_speed(self, speed):
        """设置电机速度"""
        print(f"设置电机速度: {speed}")
        # 实际项目中这里会设置电机速度
        
    def steer(self, direction):
        """根据方向值转向 (-100 到 100)"""
        if direction < -20:
            self.turn_left(abs(direction) // 2)
        elif direction > 20:
            self.turn_right(direction // 2)
        else:
            self.forward()
            
    def stop(self):
        """停止所有电机"""
        print("电机停止")
        # 实际项目中这里会停止电机
        
    def emergency_stop(self):
        """紧急停止 - 立即断电"""
        print("紧急停止！")
        # 实际项目中这里会切断电机电源    