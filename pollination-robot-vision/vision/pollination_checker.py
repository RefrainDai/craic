import cv2
import numpy as np

class PollinationChecker:
    """授粉验证类，负责检查授粉是否成功"""
    
    def __init__(self, config):
        self.config = config
        
    def check(self, frame, flower):
        """检查花朵是否授粉成功"""
        if flower["type"] != "female":
            return False
            
        # 获取花朵位置和轮廓
        cx, cy = flower["position"]
        contour = flower["contour"]
        
        # 创建掩码，只关注花朵区域
        mask = np.zeros_like(frame[:, :, 0])
        cv2.drawContours(mask, [contour], -1, 255, -1)
        
        # 检查白色标记（假设授粉标记为白色）
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 白色阈值（根据实际标记颜色调整）
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # 只保留花朵区域内的白色部分
        pollination_mask = cv2.bitwise_and(white_mask, white_mask, mask=mask)
        
        # 计算白色像素数量
        white_pixels = cv2.countNonZero(pollination_mask)
        
        # 判断是否授粉成功（根据实际情况调整阈值）
        return white_pixels > self.config.MIN_SUCCESSFUL_POLLINATION_PIXELS    