import time

class StateMachine:
    """控制授粉机器人的状态转换和行为"""
    
    # 定义状态常量
    STATES = {
        "START": 0,
        "FOLLOW_LANE": 1,
        "DETECT_FLOWER": 2,
        "APPROACH_FLOWER": 3,
        "POLLINATE": 4,
        "RETURN_LANE": 5,
        "FINISH": 6
    }
    
    def __init__(self, motor, camera, flower_detector, pollination_checker, 
                 target_locator, obstacle_detector, lane_follower, config):
        self.motor = motor
        self.camera = camera
        self.flower_detector = flower_detector
        self.pollination_checker = pollination_checker
        self.target_locator = target_locator
        self.obstacle_detector = obstacle_detector
        self.lane_follower = lane_follower
        self.config = config
        
        self.current_state = self.STATES["START"]
        self.pollination_count = 0
        self.last_flower = None
        self.start_time = time.time()
        self.lane_lost_count = 0
        
    def update(self):
        """根据当前状态执行相应的动作并处理状态转换"""
        frame = self.camera.read()
        
        if self.current_state == self.STATES["START"]:
            # 初始化并开始巡线
            self.motor.forward(self.config.MOTOR_SPEED)
            self.current_state = self.STATES["FOLLOW_LANE"]
            print("进入巡线状态")
            
        elif self.current_state == self.STATES["FOLLOW_LANE"]:
            # 巡线逻辑
            lane_direction = self.lane_follower.detect_lane(frame)
            
            if lane_direction is not None:
                self.lane_lost_count = 0
                self.motor.steer(lane_direction)
                
                # 检测花朵
                flowers = self.flower_detector.detect(frame)
                female_flowers = [f for f in flowers if f["type"] == "female"]
                
                if female_flowers:
                    # 选择最佳目标花朵 (面积最大的)
                    self.last_flower = max(female_flowers, key=lambda f: f["area"])
                    self.current_state = self.STATES["DETECT_FLOWER"]
                    self.motor.set_speed(self.config.APPROACH_SPEED)
                    print("发现雌花，准备接近")
            else:
                # 丢失赛道
                self.lane_lost_count += 1
                if self.lane_lost_count > 10:
                    print("丢失赛道，尝试旋转寻找")
                    self.motor.rotate(self.config.ROTATION_SPEED)
                    self.lane_lost_count = 0
            
        elif self.current_state == self.STATES["DETECT_FLOWER"]:
            # 精确定位花朵
            flowers = self.flower_detector.detect(frame)
            female_flowers = [f for f in flowers if f["type"] == "female"]
            
            if not female_flowers:
                # 丢失目标，返回巡线
                self.current_state = self.STATES["FOLLOW_LANE"]
                self.motor.set_speed(self.config.MOTOR_SPEED)
                print("丢失花朵目标，返回巡线")
                return
                
            # 选择最佳目标
            best_flower = self.target_locator.locate(frame, female_flowers)
            if best_flower:
                self.last_flower = best_flower
                self.current_state = self.STATES["APPROACH_FLOWER"]
                print("锁定花朵，开始接近")
                
        elif self.current_state == self.STATES["APPROACH_FLOWER"]:
            # 接近花朵
            flower_pos = self.last_flower["position"]
            frame_center = (self.config.CAMERA_WIDTH // 2, self.config.CAMERA_HEIGHT // 2)
            
            # 计算花朵与图像中心的偏移
            offset_x = flower_pos[0] - frame_center[0]
            offset_y = flower_pos[1] - frame_center[1]
            
            # 横向调整
            if abs(offset_x) > 50:  # 阈值可调整
                if offset_x < 0:
                    self.motor.turn_left()  # 向左转
                else:
                    self.motor.turn_right()  # 向右转
            else:
                # 横向对齐，前进
                self.motor.forward()
                
            # 判断是否到达授粉位置
            if offset_y < -100:  # 阈值可调整
                self.motor.stop()
                self.current_state = self.STATES["POLLINATE"]
                print("到达授粉位置，准备授粉")
                
        elif self.current_state == self.STATES["POLLINATE"]:
            # 控制机械臂进行授粉
            success = self.arm.pollinate(self.last_flower)
            if success:
                self.pollination_count += 1
                print(f"授粉成功！已完成 {self.pollination_count}/{self.config.TOTAL_FEMALE_FLOWERS} 次授粉")
                
                # 检查是否完成所有授粉任务
                if self.pollination_count >= self.config.TOTAL_FEMALE_FLOWERS:
                    self.current_state = self.STATES["FINISH"]
                    print("所有花朵授粉完成，前往终点！")
                else:
                    self.current_state = self.STATES["RETURN_LANE"]
                    self.motor.backward(duration=1.0)  # 后退一点
            else:
                print("授粉失败，尝试重新定位")
                self.current_state = self.STATES["DETECT_FLOWER"]
                
        elif self.current_state == self.STATES["RETURN_LANE"]:
            # 转回赛道
            self.motor.rotate(self.config.ROTATION_SPEED, duration=1.5)  # 旋转180度
            self.current_state = self.STATES["FOLLOW_LANE"]
            self.motor.set_speed(self.config.MOTOR_SPEED)
            print("返回赛道，继续巡线")
            
        elif self.current_state == self.STATES["FINISH"]:
            # 完成所有任务，返回起点或停止
            print("比赛完成！")
            self.motor.stop()
            
    def is_time_up(self):
        """检查是否超过比赛时间限制"""
        return (time.time() - self.start_time) > self.config.MAX_RUNNING_TIME
        
    def is_mission_complete(self):
        """检查是否完成所有授粉任务"""
        return self.pollination_count >= self.config.TOTAL_FEMALE_FLOWERS    