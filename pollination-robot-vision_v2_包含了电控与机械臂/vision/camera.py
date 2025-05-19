import cv2

class Camera:
    """摄像头接口，用于捕获图像"""
    
    def __init__(self, camera_id=0, width=640, height=480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        
    def __enter__(self):
        self.open()
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        
    def open(self):
        """打开摄像头"""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise ValueError(f"无法打开摄像头 {self.camera_id}")
            
        # 设置摄像头分辨率
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        print(f"摄像头已打开: {self.camera_id} ({self.width}x{self.height})")
        
    def read(self):
        """读取一帧图像"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return frame if ret else None
        return None
        
    def release(self):
        """释放摄像头资源"""
        if self.cap:
            self.cap.release()
            print("摄像头资源已释放")    