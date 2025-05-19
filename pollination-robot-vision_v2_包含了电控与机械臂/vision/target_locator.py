class TargetLocator:
    """定位最佳目标花朵"""
    
    def __init__(self, config):
        self.config = config
        
    def locate(self, frame, flowers):
        """从多个花朵中选择最佳目标"""
        if not flowers:
            return None
            
        # 计算每个花朵的优先级
        # 这里使用花朵大小和位置作为优先级因素
        frame_center = (self.config.CAMERA_WIDTH // 2, self.config.CAMERA_HEIGHT // 2)
        
        best_flower = None
        highest_score = -1
        
        for flower in flowers:
            # 花朵中心与图像中心的距离
            distance = abs(flower["position"][0] - frame_center[0])
            
            # 花朵面积作为权重
            area = flower["area"]
            
            # 计算分数 (面积越大、越居中的花朵分数越高)
            score = area - (distance * 2)  # 距离的权重较低
            
            if score > highest_score:
                highest_score = score
                best_flower = flower
                
        return best_flower    