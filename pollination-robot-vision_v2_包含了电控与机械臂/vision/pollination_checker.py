import cv2
import numpy as np

class PollinationChecker:
    """检查花朵是否已经授粉"""
    
    def __init__(self, config):
        self.config = config
        
    def check(self, frame, flower_position):
        """检查指定位置的花朵是否已授粉"""
        if frame is None:
            return False
            
        x, y = flower_position
        
        # 创建花朵周围的感兴趣区域(ROI)
        roi_size = 50
        x1 = max(0, x - roi_size)
        y1 = max(0, y - roi_size)
        x2 = min(frame.shape[1], x + roi_size)
        y2 = min(frame.shape[0], y + roi_size)
        
        roi = frame[y1:y2, x1:x2]
        
        if roi.size == 0:
            return False
            
        # 转换到HSV颜色空间
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 创建白色掩码（授粉标记）
        white_mask = cv2.inRange(hsv, 
                                self.config.WHITE_LOWER, 
                                self.config.WHITE_UPPER)
                                
        # 计算白色区域比例
        white_pixels = cv2.countNonZero(white_mask)
        total_pixels = roi.shape[0] * roi.shape[1]
        
        # 如果白色区域比例超过阈值，则认为已授粉
        return (white_pixels / total_pixels) > 0.1    