import cv2
import numpy as np

class FlowerDetector:
    """检测和识别花朵"""
    
    def __init__(self, config):
        self.config = config
        self.erode_kernel = np.ones(self.config.ERODE_KERNEL, np.uint8)
        self.dilate_kernel = np.ones(self.config.DILATE_KERNEL, np.uint8)
        
    def detect(self, frame):
        """检测图像中的花朵"""
        if frame is None:
            return []
            
        # 转换到HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 创建黄色掩码（雌花特征）
        yellow_mask = cv2.inRange(hsv, 
                                 self.config.YELLOW_LOWER, 
                                 self.config.YELLOW_UPPER)
                                 
        # 创建白色掩码（雄花/授粉标记）
        white_mask = cv2.inRange(hsv, 
                                self.config.WHITE_LOWER, 
                                self.config.WHITE_UPPER)
                                
        # 形态学操作
        yellow_mask = cv2.erode(yellow_mask, self.erode_kernel, iterations=self.config.ERODE_ITERATIONS)
        yellow_mask = cv2.dilate(yellow_mask, self.dilate_kernel, iterations=self.config.DILATE_ITERATIONS)
        
        white_mask = cv2.erode(white_mask, self.erode_kernel, iterations=self.config.ERODE_ITERATIONS)
        white_mask = cv2.dilate(white_mask, self.dilate_kernel, iterations=self.config.DILATE_ITERATIONS)
        
        # 查找轮廓
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        white_contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤并分类花朵
        flowers = []
        
        # 处理雌花
        for cnt in yellow_contours:
            area = cv2.contourArea(cnt)
            if self.config.MIN_FLOWER_AREA < area < self.config.MAX_FLOWER_AREA:
                # 计算轮廓中心
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    flowers.append({
                        "type": "female",
                        "position": (cX, cY),
                        "area": area,
                        "contour": cnt
                    })
                    
        # 处理雄花
        for cnt in white_contours:
            area = cv2.contourArea(cnt)
            if self.config.MIN_FLOWER_AREA < area < self.config.MAX_FLOWER_AREA:
                # 计算轮廓中心
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    flowers.append({
                        "type": "male",
                        "position": (cX, cY),
                        "area": area,
                        "contour": cnt
                    })
                    
        return flowers    