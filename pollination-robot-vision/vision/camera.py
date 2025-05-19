import cv2

class Camera:
    """摄像头控制类，负责图像采集"""
    
    def __init__(self, camera_id=0, width=640, height=480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        
    def open(self):
        """打开摄像头"""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise IOError(f"无法打开摄像头 {self.camera_id}")
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return True
        
    def read(self):
        """读取一帧图像"""
        if self.cap is None or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        return frame if ret else None
        
    def release(self):
        """释放摄像头资源"""
        if self.cap:
            self.cap.release()
            self.cap = None
            
    def __enter__(self):
        self.open()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()    