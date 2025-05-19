import argparse
import logging
import cv2
from config.config import Config
from config.config_competition import CompetitionConfig
from vision.camera import Camera
from vision.flower_detector import FlowerDetector
from vision.pollination_checker import PollinationChecker
from vision.target_locator import TargetLocator
from vision.obstacle_detector import ObstacleDetector
from navigation.lane_follower import LaneFollower
from control.motor import MotorController
from control.arm import ArmController
from control.state_machine import StateMachine
from utils.visualization import Visualizer
from utils.logger import setup_logger

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='授粉机器人控制系统')
    parser.add_argument('--mode', type=str, default='debug', choices=['debug', 'competition'],
                        help='运行模式：debug（调试）或competition（比赛）')
    args = parser.parse_args()
    
    # 根据模式选择配置
    config = CompetitionConfig() if args.mode == 'competition' else Config()
    
    # 设置日志
    logger = setup_logger('pollination_robot', level=getattr(logging, config.LOG_LEVEL), 
                         log_file=config.LOG_FILE if args.mode == 'competition' else None)
    logger.info(f"机器人启动，运行模式: {args.mode}")
    
    try:
        # 初始化硬件和算法模块
        with Camera(config.CAMERA_ID, config.CAMERA_WIDTH, config.CAMERA_HEIGHT) as camera, \
             MotorController(config) as motor, \
             ArmController(config) as arm:
            
            camera.open()
            
            flower_detector = FlowerDetector(config)
            pollination_checker = PollinationChecker(config)
            target_locator = TargetLocator(config)
            obstacle_detector = ObstacleDetector(config)
            lane_follower = LaneFollower(config)
            
            # 初始化状态机
            state_machine = StateMachine(
                motor=motor,
                camera=camera,
                flower_detector=flower_detector,
                pollination_checker=pollination_checker,
                target_locator=target_locator,
                obstacle_detector=obstacle_detector,
                lane_follower=lane_follower,
                config=config
            )
            
            # 校准机械臂
            arm.calibrate()
            
            # 启动计时器
            start_time = time.time()
            
            # 主循环
            while not state_machine.is_mission_complete() and not state_machine.is_time_up():
                try:
                    # 更新状态机
                    state_machine.update()
                    
                    # 可视化（调试模式）
                    if config.DEBUG_MODE:
                        frame = camera.read()
                        if frame is not None:
                            # 绘制花朵和障碍物
                            flowers = flower_detector.detect(frame)
                            obstacles = obstacle_detector.detect(frame)
                            
                            result_frame = Visualizer.draw_flowers(frame, flowers)
                            result_frame = Visualizer.draw_obstacles(result_frame, obstacles)
                            
                            # 绘制车道信息
                            lane_error = lane_follower.detect_lane(frame)
                            result_frame = Visualizer.draw_lane(result_frame, lane_error)
                            
                            # 显示状态信息
                            cv2.putText(result_frame, f"State: {list(StateMachine.STATES.keys())[list(StateMachine.STATES.values()).index(state_machine.current_state)]}", 
                                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            cv2.putText(result_frame, f"Pollinations: {state_machine.pollination_count}/{config.TOTAL_FEMALE_FLOWERS}", 
                                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            cv2.putText(result_frame, f"Time: {time.time()-start_time:.1f}s / {config.MAX_RUNNING_TIME}s", 
                                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            
                            # 显示结果
                            cv2.imshow("Pollination Robot Vision", result_frame)
                            
                            # 按q键退出（调试模式）
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                                
                except Exception as e:
                    logger.error(f"主循环异常: {e}")
                    # 发生异常时继续运行，避免程序崩溃
                    time.sleep(0.1)
            
            # 任务完成或时间结束
            logger.info(f"任务完成！总授粉数: {state_machine.pollination_count}")
            
    except Exception as e:
        logger.critical(f"系统错误: {e}", exc_info=True)
        # 紧急停止电机
        try:
            motor.emergency_stop()
        except:
            pass
    finally:
        # 清理资源
        cv2.destroyAllWindows()
        logger.info("系统已关闭")

if __name__ == "__main__":
    import time  # 确保time模块已导入
    main()    