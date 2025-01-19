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

def calculate_correlation(df, target_column, columns_to_check):
    correlation_results = {}
    for column in columns_to_check:
        if column in df.columns:
            correlation = df[column].dropna().corr(df[target_column].dropna())
            correlation_results[column] = correlation
    return correlation_results

def save_correlation_to_excel(correlation_results, output_path):
    correlation_df = pd.DataFrame(list(correlation_results.items()), columns=['特征', '相关系数'])
    correlation_df.to_excel(output_path, index=False)

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

# 读取提供的区域数据
area_data = {
    '区域': ['农安县', '榆树市', '绿园区', '德惠市', '宽城区', '南关区', '朝阳区', '九台区', '二道区', '双阳区'],
    '人口': [1101671, 1178338, 715000, 858800, 674200, 662300, 617000, 563400, 320634, 350643],
    '人均（万/人）': [2.795, 2.301, 3.889, 3.280, 4.628, 7.337, 13.546, 4.483, 7.226, 4.791]
}
area_df = pd.DataFrame(area_data)

# 合并数据
merged_df = df.merge(area_df, left_on='Class', right_on='区域', how='left')

# 计算相关系数
target_column = 'Price (USD)'
columns_to_check = ['人口', '人均（万/人）']
correlation_results = calculate_correlation(merged_df, target_column, columns_to_check)

# 输出相关系数到 Excel
output_path = "C:/Users/Herzog/Desktop/2025美赛/数据/相关系数1.xlsx"
save_correlation_to_excel(correlation_results, output_path)

print("相关系数已保存到:", output_path)