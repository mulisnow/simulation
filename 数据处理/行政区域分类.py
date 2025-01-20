import pandas as pd
import os
import json

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
    if not polygon or not isinstance(polygon[0], (list, tuple)) or len(polygon[0]) != 2:
        return False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def classify_points(df, geo_data):
    df['Class'] = None
    for class_name, data in geo_data.items():
        coordinates = data['geometry']['coordinates']
        if coordinates:
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

# 主程序
geo_folder_path = "C:/Users/Herzog/Desktop/2025美赛/数据/城市2行政区经纬度"
geo_data = load_geo_data(geo_folder_path)

data_file_path = "C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 2_城市2待 售 房 产 的 基 本 信 息.xlsx"
df = pd.read_excel(data_file_path)

# 确保经纬度列为数值类型
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')

# 分类经纬度
df = classify_points(df, geo_data)

# 创建输出目录
output_folder = "C:/Users/Herzog/Desktop/2025美赛/数据/城市2"
os.makedirs(output_folder, exist_ok=True)

# 根据类名保存数据
classes = df['Class'].unique()  # 获取所有唯一的类名
for class_name in classes:
    class_data = df[df['Class'] == class_name]
    if not class_data.empty:  # 确保类名下有数据
        output_path = os.path.join(output_folder, f"{class_name}.xlsx")
        class_data.to_excel(output_path, index=False)
        print(f"类名: {class_name} 的数据已保存到: {output_path}")
    else:
        print(f"类名: {class_name} 没有数据，未保存。") 