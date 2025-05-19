# test_flower_detection.py
import cv2
import argparse
import os
from config.config import Config
from vision.flower_detector import FlowerDetector
from utils.visualization import Visualizer

def main():
    parser = argparse.ArgumentParser(description='测试花朵识别算法')
    parser.add_argument('--image', type=str, help='测试图片路径')
    parser.add_argument('--folder', type=str, help='测试图片文件夹路径')
    parser.add_argument('--mode', type=str, default='debug', choices=['debug', 'competition'],
                        help='运行模式：debug（调试）或competition（比赛）')
    args = parser.parse_args()
    
    # 根据模式选择配置
    config = Config() if args.mode == 'debug' else CompetitionConfig()
    
    # 初始化花朵检测器
    detector = FlowerDetector(config)
    
    # 处理单张图片
    if args.image:
        if os.path.exists(args.image):
            process_image(args.image, detector, config)
        else:
            print(f"错误：图片 '{args.image}' 不存在")
    
    # 处理文件夹中的所有图片
    elif args.folder:
        if os.path.exists(args.folder):
            for filename in os.listdir(args.folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(args.folder, filename)
                    process_image(image_path, detector, config)
        else:
            print(f"错误：文件夹 '{args.folder}' 不存在")
    
    else:
        print("请提供 --image 或 --folder 参数")

def process_image(image_path, detector, config):
    """处理单张图片并显示检测结果"""
    # 读取图片
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"无法读取图片: {image_path}")
        return
    
    # 检测花朵
    flowers = detector.detect(frame)
    
    # 可视化结果
    result_frame = Visualizer.draw_flowers(frame, flowers)
    
    # 显示结果
    window_name = os.path.basename(image_path)
    cv2.imshow(window_name, result_frame)
    
    # 保存结果（可选）
    output_path = image_path.replace('.', '_detected.')
    cv2.imwrite(output_path, result_frame)
    print(f"结果已保存至: {output_path}")
    
    # 按任意键继续
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)

if __name__ == "__main__":
    from config.config_competition import CompetitionConfig
    main()