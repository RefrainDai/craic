import cv2
import numpy as np

class LaneFollower:
    """巡线控制模块"""
    
    def __init__(self, config):
        self.config = config
        
    def detect_lane(self, frame):
        """检测赛道并计算转向方向"""
        if frame is None:
            return None
            
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 二值化
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # 只关注图像下半部分（赛道通常在下方）
        height, width = binary.shape
        roi = binary[int(height*0.6):height, 0:width]
        
        # 计算图像中心和质心
        M = cv2.moments(roi)
        
        if M["m00"] != 0:
            # 计算质心
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # 计算质心与图像中心的偏移
            frame_center = width // 2
            error = cX - frame_center
            
            # 返回偏移量作为转向控制依据
            # 负值表示向左偏，正值表示向右偏
            return error
            
        return None  # 无法检测到线    