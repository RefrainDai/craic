# auto_tune_thresholds.py (无tqdm和sklearn)
import cv2
import numpy as np
import os
import argparse
from collections import defaultdict

class ThresholdTuner:
    def __init__(self):
        self.results = defaultdict(dict)  # 按类别存储最优阈值
        
    def process_image_folder(self, image_folder, categories=None):
        """处理图片文件夹，按类别提取阈值"""
        if not categories:
            # 默认按光照强度分类
            categories = ["bright", "medium", "dark"]
            
        # 扫描所有图片
        for filename in os.listdir(image_folder):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            image_path = os.path.join(image_folder, filename)
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"警告: 无法读取图片 {image_path}")
                continue
                
            # 自动分类（基于亮度）
            category = self._classify_image(image, categories)
            
            # 提取花朵像素
            yellow_pixels = self._extract_flower_pixels(image, flower_type="female")
            white_pixels = self._extract_flower_pixels(image, flower_type="male")
            
            # 更新该类别的颜色统计
            self._update_category_stats(category, yellow_pixels, white_pixels)
        
        # 为每个类别计算最终阈值
        self._calculate_final_thresholds()
        
        return self.results
    
    def _classify_image(self, image, categories):
        """基于亮度对图片进行分类"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness > 180:
            return categories[0]  # "bright"
        elif brightness < 80:
            return categories[2]  # "dark"
        else:
            return categories[1]  # "medium"
    
    def _extract_flower_pixels(self, image, flower_type="female"):
        """提取花朵像素（基于初始估计的阈值）"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 初始阈值（可根据需要调整）
        if flower_type == "female":  # 黄色花
            lower = np.array([15, 80, 80])
            upper = np.array([35, 255, 255])
        else:  # 白色花
            lower = np.array([0, 0, 180])
            upper = np.array([180, 30, 255])
        
        # 创建掩码
        mask = cv2.inRange(hsv, lower, upper)
        
        # 应用形态学操作过滤噪声
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # 提取掩码区域的像素
        pixels = hsv[mask > 0]
        return pixels
    
    def _update_category_stats(self, category, yellow_pixels, white_pixels):
        """更新每个类别的颜色统计"""
        # 初始化类别统计
        if "yellow" not in self.results[category]:
            self.results[category]["yellow"] = []
        if "white" not in self.results[category]:
            self.results[category]["white"] = []
        
        # 添加当前图片的像素
        if len(yellow_pixels) > 0:
            self.results[category]["yellow"].append(yellow_pixels)
        if len(white_pixels) > 0:
            self.results[category]["white"].append(white_pixels)
    
    def _calculate_final_thresholds(self):
        """为每个类别计算最终的HSV阈值"""
        for category, colors in self.results.items():
            for color_name, pixel_list in colors.items():
                if not pixel_list:
                    continue
                    
                # 合并所有像素
                pixels = np.vstack(pixel_list)
                
                # 计算HSV各通道的均值和标准差
                h_mean, s_mean, v_mean = np.mean(pixels, axis=0)
                h_std, s_std, v_std = np.std(pixels, axis=0)
                
                # 基于均值和标准差确定阈值范围
                # 调整系数可控制阈值的宽窄（1.5-2.0通常效果较好）
                h_min = max(0, int(h_mean - h_std * 1.8))
                h_max = min(180, int(h_mean + h_std * 1.8))
                s_min = max(0, int(s_mean - s_std * 1.5))
                s_max = min(255, int(s_mean + s_std * 1.5))
                v_min = max(0, int(v_mean - s_std * 1.5))
                v_max = min(255, int(v_mean + s_std * 1.5))
                
                # 特殊处理白色花朵（低饱和度）
                if color_name == "white":
                    s_max = min(50, s_max)  # 限制白色的最大饱和度
                
                # 保存阈值
                self.results[category][color_name] = {
                    "lower": (h_min, s_min, v_min),
                    "upper": (h_max, s_max, v_max)
                }
    
    def save_config(self, output_file="auto_thresholds.py"):
        """保存配置到Python文件"""
        with open(output_file, "w") as f:
            f.write("# 自动生成的HSV阈值配置\n")
            f.write("# 基于测试图片分类计算\n\n")
            
            for category, colors in self.results.items():
                f.write(f"# {category} 光照条件下的阈值\n")
                
                for color_name, thresholds in colors.items():
                    if isinstance(thresholds, dict):  # 已计算的阈值
                        lower = thresholds["lower"]
                        upper = thresholds["upper"]
                        
                        var_name_lower = f"{color_name.upper()}_LOWER_{category.upper()}"
                        var_name_upper = f"{color_name.upper()}_UPPER_{category.upper()}"
                        
                        f.write(f"{var_name_lower} = ({lower[0]}, {lower[1]}, {lower[2]})\n")
                        f.write(f"{var_name_upper} = ({upper[0]}, {upper[1]}, {upper[2]})\n")
                
                f.write("\n")  # 空行分隔不同类别
    
    def print_results(self):
        """打印计算结果"""
        for category, colors in self.results.items():
            print(f"\n=== {category.upper()} 光照条件 ===")
            
            for color_name, thresholds in colors.items():
                if isinstance(thresholds, dict):  # 已计算的阈值
                    print(f"{color_name.upper()} 花朵:")
                    print(f"  下限: {thresholds['lower']}")
                    print(f"  上限: {thresholds['upper']}")

def main():
    parser = argparse.ArgumentParser(description='自动提取不同类别图片的HSV阈值')
    parser.add_argument('--folder', type=str, required=True, help='测试图片文件夹路径')
    parser.add_argument('--output', type=str, default='auto_thresholds.py', help='输出配置文件路径')
    args = parser.parse_args()
    
    tuner = ThresholdTuner()
    tuner.process_image_folder(args.folder)
    tuner.print_results()
    tuner.save_config(args.output)
    
    print(f"\n配置已保存到: {args.output}")
    print("请将生成的阈值复制到config.py中使用")

if __name__ == "__main__":
    main()