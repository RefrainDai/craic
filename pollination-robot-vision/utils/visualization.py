import cv2

class Visualizer:
    """可视化工具类，用于显示检测结果"""
    
    @staticmethod
    def draw_flowers(frame, flowers):
        """在图像上绘制花朵"""
        if frame is None:
            return None
            
        result = frame.copy()
        
        for flower in flowers:
            cx, cy = flower["position"]
            color = (0, 255, 0) if flower["type"] == "female" else (0, 0, 255)
            
            # 绘制轮廓
            cv2.drawContours(result, [flower["contour"]], -1, color, 2)
            
            # 绘制中心
            cv2.circle(result, (cx, cy), 5, color, -1)
            
            # 添加标签
            label = f"{flower['type']} ({int(flower['area'])})"
            cv2.putText(result, label, (cx-30, cy-30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
        return result
        
    @staticmethod
    def draw_target(frame, target_position, flower=None):
        """在图像上绘制目标授粉点"""
        if frame is None or target_position is None:
            return frame
            
        result = frame.copy()
        tx, ty = target_position
        
        # 绘制目标点
        cv2.circle(result, (tx, ty), 10, (255, 0, 0), 2)
        cv2.line(result, (tx-15, ty), (tx+15, ty), (255, 0, 0), 2)
        cv2.line(result, (tx, ty-15), (tx, ty+15), (255, 0, 0), 2)
        
        # 如果有对应的花朵，绘制连接线
        if flower:
            fx, fy = flower["position"]
            cv2.line(result, (fx, fy), (tx, ty), (255, 0, 0), 2)
            
        return result
        
    @staticmethod
    def draw_obstacles(frame, obstacles):
        """在图像上绘制障碍物"""
        if frame is None:
            return None
            
        result = frame.copy()
        
        for obstacle in obstacles:
            x1, y1, x2, y2 = obstacle["bounding_box"]
            
            # 绘制边界框
            cv2.rectangle(result, (x1, y1), (x2, y2), (0, 165, 255), 2)
            
            # 添加标签
            label = f"Obstacle ({int(obstacle['area'])})"
            cv2.putText(result, label, (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            
        return result    