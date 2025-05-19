import cv2
import numpy as np

class FlowerDetector:
    """花朵识别类，负责区分雌花、雄花和雌雄同体花"""
    
    def __init__(self, config):
        self.config = config
        
    def detect(self, frame):
        """检测图像中的花朵并分类"""
        if frame is None:
            return []
            
        # 预处理图像
        processed_frame = self._preprocess(frame)
        
        # 检测花朵轮廓
        contours = self._detect_contours(processed_frame)
        
        # 分类花朵类型
        flowers = self._classify_flowers(frame, contours)
        
        return flowers
        
    def _preprocess(self, frame):
        """图像预处理"""
        # 转换为HSV颜色空间便于颜色检测
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 高斯模糊减少噪声
        blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
        
        return blurred
        
    def _detect_contours(self, frame):
        """检测花朵轮廓"""
        # 创建黄色掩码（根据实际花朵颜色调整）
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(frame, lower_yellow, upper_yellow)
        
        # 边缘检测
        edges = cv2.Canny(yellow_mask, 50, 150)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        return contours
        
    def _classify_flowers(self, frame, contours):
        """根据轮廓特征分类花朵类型"""
        flowers = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # 过滤过小或过大的轮廓
            if area < self.config.MIN_FLOWER_AREA or area > self.config.MAX_FLOWER_AREA:
                continue
                
            # 计算轮廓中心
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # 判断花朵类型
                flower_type = self._determine_flower_type(frame, contour)
                
                flowers.append({
                    "type": flower_type,
                    "position": (cX, cY),
                    "area": area,
                    "contour": contour
                })
                
        return flowers
        
    def _determine_flower_type(self, frame, contour):
        """根据花朵特征确定类型（雌花、雄花或未知）"""
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        roi = frame[y:y+h, x:x+w]
        
        # 计算黄色像素比例（雌花中心黄色区域较大）
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv_roi, 
                                  np.array([20, 100, 100]), 
                                  np.array([30, 255, 255]))
        yellow_ratio = np.count_nonzero(yellow_mask) / (w * h)
        
        # 根据黄色比例和形状特征判断花朵类型
        if yellow_ratio > self.config.FEMALE_YELLOW_RATIO:
            return "female"
        else:
            return "male"    