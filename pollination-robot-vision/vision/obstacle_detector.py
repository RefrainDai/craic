import cv2
import numpy as np

class ObstacleDetector:
    """障碍物检测类，负责识别场地中的障碍物"""
    
    def __init__(self, config):
        self.config = config
        
    def detect(self, frame):
        """检测图像中的障碍物"""
        if frame is None:
            return []
            
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 创建黑色障碍物掩码（根据实际障碍物颜色调整）
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 30])
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        black_mask = cv2.inRange(hsv, lower_black, upper_black)
        
        # 查找轮廓
        contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        obstacles = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # 过滤过小的轮廓
            if area < self.config.MIN_OBSTACLE_AREA:
                continue
                
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            obstacles.append({
                "position": (x + w//2, y + h//2),
                "size": (w, h),
                "area": area,
                "bounding_box": (x, y, x+w, y+h)
            })
            
        return obstacles    