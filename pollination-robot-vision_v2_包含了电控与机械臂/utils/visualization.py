import cv2

class Visualizer:
    """可视化工具，用于调试和显示结果"""
    
    @staticmethod
    def draw_flowers(frame, flowers):
        """在图像上绘制花朵"""
        if frame is None:
            return None
            
        result = frame.copy()
        
        for flower in flowers:
            x, y = flower["position"]
            color = (0, 255, 0) if flower["type"] == "female" else (255, 0, 0)
            
            # 绘制中心点
            cv2.circle(result, (x, y), 5, color, -1)
            
            # 绘制轮廓
            cv2.drawContours(result, [flower["contour"]], -1, color, 2)
            
            # 添加标签
            label = f"{flower['type']} ({flower['area']})"
            cv2.putText(result, label, (x-20, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                       
        return result
        
    @staticmethod
    def draw_obstacles(frame, obstacles):
        """在图像上绘制障碍物"""
        if frame is None:
            return None
            
        result = frame.copy()
        
        for obstacle in obstacles:
            x, y, w, h = obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]
            
            # 绘制边界框
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
            # 添加标签
            label = f"Obstacle ({obstacle['area']})"
            cv2.putText(result, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                       
        return result
        
    @staticmethod
    def draw_lane(frame, error):
        """在图像上绘制车道和转向信息"""
        if frame is None:
            return None
            
        result = frame.copy()
        height, width = result.shape[:2]
        
        # 绘制中心线
        cv2.line(result, (width//2, 0), (width//2, height), (255, 255, 0), 2)
        
        # 绘制转向信息
        if error is not None:
            direction = "Left" if error < 0 else "Right"
            magnitude = abs(error)
            
            # 绘制偏移指示
            cv2.arrowedLine(result, (width//2, height-50), 
                           (width//2 + error, height-50), 
                           (0, 255, 255), 3)
                           
            # 添加文本
            text = f"Steer: {direction} ({magnitude})"
            cv2.putText(result, text, (10, height-20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                       
        return result    