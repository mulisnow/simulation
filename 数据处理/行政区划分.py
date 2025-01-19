import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import re


def load_geo_data(folder_path):
    geo_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                geo_data[filename[:-5]] = json.load(file)  # 去掉.json 后缀
    return geo_data


def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    # 确保 polygon 不为空且第一个元素是可迭代对象且长度为 2
    if not polygon or not isinstance(polygon[0], (list, tuple)) or len(polygon[0])!= 2:
        return False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y!= p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def classify_points(df, geo_data):
    df['Class'] = None
    for class_name, data in geo_data.items():
        # 处理多边形坐标
        coordinates = data['geometry']['coordinates']
        if coordinates:  # 确保有坐标数据
            # 考虑 coordinates 中可能包含多个子多边形的情况
            if isinstance(coordinates[0], list):
                for sub_polygon in coordinates:
                    for index, row in df.iterrows():
                        point = (row['lon'], row['lat'])
                        if is_point_in_polygon(point, sub_polygon):
                            df.at[index, 'Class'] = class_name
            else:
                for index, row in df.iterrows():
                    point = (row['lon'], row['lat'])
                    if is_point_in_polygon(point, coordinates):
                        df.at[index, 'Class'] = class_name
    return df


def plot_data(df, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 设置字体以支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    # 选择需要绘制的列
    y_columns = [
        'Total number of households',
        'Greening rate',
        'Floor area ratio',
        'Building type',
        'parking space',
        'Property management fee（/m²/month USD）',
        'above-ground parking fee（/month USD）',
        'underground parking fee（/month USD）'
    ]
    # 中文翻译字典
    translation_dict = {
        'Total number of households': '总户数',
        'Greening rate': '绿化率',
        'Floor area ratio': '容积率',
        'Building type': '建筑类型',
        'parking space': '停车位',
        'Property management fee（/m²/month USD）': '物业管理费（/m²/月 USD）',
        'above-ground parking fee（/month USD）': '地上停车费（/月 USD）',
        'underground parking fee（/month USD）': '地下停车费（/月 USD）'
    }
    # 按类绘制散点图
    for class_name, group in df.groupby('Class'):
        if class_name is not None:  # 确保类名不为空
            class_dir = os.path.join(output_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            for column in y_columns:
                if column in group.columns:  # 确保列存在
                    # 确保 Y 轴列为数值类型
                    group[column] = pd.to_numeric(group[column], errors='coerce')
                    plt.figure(figsize=(12, 6))
                    plt.scatter(group['Price (USD)'], group[column], label=column, alpha=0.6)
                    plt.title(f'价格与{translation_dict[column]}的关系 - 类别: {class_name}')
                    plt.xlabel('价格 (USD)')
                    plt.ylabel(translation_dict[column])
                    plt.legend()
                    plt.grid()
                    # 清理文件名，替换非法字符
                    safe_column_name = re.sub(r'[<>:"/\\|?*]', '_', translation_dict[column])
                    output_file_path = os.path.join(class_dir, f'价格_vs_{safe_column_name}.png')
                    plt.savefig(output_file_path)
                    plt.close()  # 关闭图形以释放内存


# 主程序
geo_folder_path = "C:/Users/Herzog/Desktop/2025美赛/数据/城市1行政区域经纬度"
geo_data = load_geo_data(geo_folder_path)
data_file_path = "C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 1_城市1待 售 房 产 的 基 本 信 息.xlsx"
df = pd.read_excel(data_file_path)
# 确保经纬度列为数值类型
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
# 分类经纬度
df = classify_points(df, geo_data)
# 输出图表目录
output_directory = "C:/Users/Herzog/Desktop/2025美赛/图表/城市1图"
plot_data(df, output_directory)