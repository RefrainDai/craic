from vision.camera import Camera
from vision.flower_detector import FlowerDetector
from vision.pollination_checker import PollinationChecker
from vision.target_locator import TargetLocator
from vision.obstacle_detector import ObstacleDetector
from utils.config import Config
from utils.visualization import Visualizer
import time
import cv2
def main():
    # 加载配置
    config = Config()
    
    # 初始化各模块
    with Camera(config.CAMERA_ID, config.CAMERA_WIDTH, config.CAMERA_HEIGHT) as camera:
        flower_detector = FlowerDetector(config)
        pollination_checker = PollinationChecker(config)
        target_locator = TargetLocator(config)
        obstacle_detector = ObstacleDetector(config)
        
        # 主循环
        while True:
            # 捕获图像
            frame = camera.read()
            if frame is None:
                print("无法获取图像")
                time.sleep(0.1)
                continue
                
            # 检测花朵
            start_time = time.time()
            flowers = flower_detector.detect(frame)
            detection_time = time.time() - start_time
            
            # 检测障碍物
            obstacles = obstacle_detector.detect(frame)
            
            # 定位最佳授粉点
            target_position, target_flower = target_locator.locate(frame, flowers)
            
            # 检查授粉状态（如果有目标花朵）
            pollination_status = False
            if target_flower:
                pollination_status = pollination_checker.check(frame, target_flower)
            
            # 可视化结果
            result_frame = frame.copy()
            result_frame = Visualizer.draw_flowers(result_frame, flowers)
            result_frame = Visualizer.draw_obstacles(result_frame, obstacles)
            result_frame = Visualizer.draw_target(result_frame, target_position, target_flower)
            
            # 添加状态信息
            status_text = f"Flowers: {len(flowers)}, Obstacles: {len(obstacles)}"
            status_text += f", Detection Time: {detection_time:.2f}s"
            cv2.putText(result_frame, status_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            if target_flower:
                pollination_text = "Pollination: " + ("SUCCESS" if pollination_status else "FAILED")
                cv2.putText(result_frame, pollination_text, (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                            (0, 255, 0) if pollination_status else (0, 0, 255), 2)
            
            # 显示结果
            cv2.imshow("Pollination Robot Vision", result_frame)
            
            # 按ESC或q键退出
            key = cv2.waitKey(1)
            if key == 27 or key == ord('q'):  # ESC键或q键
                break
                
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    