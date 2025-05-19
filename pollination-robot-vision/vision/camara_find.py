import cv2

def list_available_cameras():
    # 尝试索引0到9的摄像头
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"摄像头索引 {i} 可用")
            ret, frame = cap.read()
            if ret:
                print(f"  - 分辨率: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
        else:
            print(f"摄像头索引 {i} 不可用")

if __name__ == "__main__":
    list_available_cameras()