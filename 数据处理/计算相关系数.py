import pandas as pd
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

def clean_data(df, columns_to_check):
    for column in columns_to_check:
        df[column] = pd.to_numeric(df[column], errors='coerce')  # 转换为数值类型，无法转换的值将变为 NaN
    return df

def calculate_correlation(df, target_column, columns_to_check):
    correlation_results = {}
    for column in columns_to_check:
        if column in df.columns:
            # 计算相关系数，确保没有 NaN 值
            correlation = df[column].dropna().corr(df[target_column].dropna())
            correlation_results[column] = correlation
    return correlation_results

def save_correlation_to_excel(correlation_results, output_path):
    # 创建 DataFrame
    correlation_df = pd.DataFrame(list(correlation_results.items()), columns=['特征', '相关系数'])
    correlation_df.to_excel(output_path, index=False)

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

# 数据清洗
columns_to_check = [
    'Total number of households',  # 总户数
    'Greening rate',                # 绿化率
    'Floor area ratio',             # 容积率
    'Building type',                # 建筑类型
    'parking space',                # 停车位
    'Property management fee（/m²/month USD）',  # 物业管理费（/m²/月 USD）
    'above-ground parking fee（/month USD）',    # 地上停车费（/月 USD）
    'underground parking fee（/month USD）',      # 地下停车费（/月 USD）
    'Price (USD)'                   # 价格（美元）
]
df = clean_data(df, columns_to_check)

# 计算相关系数
target_column = 'Price (USD)'
correlation_results = calculate_correlation(df, target_column, columns_to_check)

# 输出相关系数到 Excel
output_path = "C:/Users/Herzog/Desktop/2025美赛/数据/相关系数.xlsx"
save_correlation_to_excel(correlation_results, output_path)

print("相关系数已保存到:", output_path) 