import cv2
import numpy as np

class ObstacleDetector:
    """检测赛道上的障碍物"""
    
    def __init__(self, config):
        self.config = config
        
    def detect(self, frame):
        """检测图像中的障碍物"""
        if frame is None:
            return []
            
        # 转换到HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 创建黑色掩码（障碍物特征）
        black_mask = cv2.inRange(hsv, 
                                self.config.BLACK_LOWER, 
                                self.config.BLACK_UPPER)
                                
        # 形态学操作
        kernel = np.ones((5, 5), np.uint8)
        black_mask = cv2.erode(black_mask, kernel, iterations=1)
        black_mask = cv2.dilate(black_mask, kernel, iterations=2)
        
        # 查找轮廓
        contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤障碍物
        obstacles = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:  # 忽略小面积区域
                x, y, w, h = cv2.boundingRect(cnt)
                obstacles.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "area": area,
                    "contour": cnt
                })
                
        return obstacles    