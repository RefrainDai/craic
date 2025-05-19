import cv2
import time

def capture_photo():
    # 初始化摄像头，0表示默认摄像头
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 等待摄像头启动并自动调整曝光度
    time.sleep(2)
    
    # 拍照前显示预览
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取画面")
            break
            
        # 显示预览画面
        cv2.imshow('Preview - Press SPACE to capture', frame)
        
        # 按空格键拍照，按ESC键退出
        key = cv2.waitKey(1)
        if key == 32:  # 空格键
            # 保存图片
            filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            print(f"照片已保存为: {filename}")
            break
        elif key == 27:  # ESC键
            break
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_photo()