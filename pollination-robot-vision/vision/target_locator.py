import cv2
import numpy as np

class TargetLocator:
    """授粉点定位类，负责确定机器人的目标位置"""
    
    def __init__(self, config):
        self.config = config
        
    def locate(self, frame, flowers):
        """确定最佳授粉点"""
        if not flowers:
            return None, None
            
        # 筛选雌花
        female_flowers = [f for f in flowers if f["type"] == "female"]
        
        if not female_flowers:
            return None, None
            
        # 根据花朵位置和大小确定最佳授粉目标
        # 这里简化为选择最大的雌花
        best_flower = max(female_flowers, key=lambda f: f["area"])
        
        # 计算授粉点（相对于花朵中心的偏移）
        cx, cy = best_flower["position"]
        target_x = cx + self.config.POLLINATION_OFFSET_X
        target_y = cy + self.config.POLLINATION_OFFSET_Y
        
        return (target_x, target_y), best_flower    