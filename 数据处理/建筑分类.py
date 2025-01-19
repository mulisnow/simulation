import pandas as pd
import os

# 定义函数来处理每个文件
def process_file(file_path):
    df = pd.read_excel(file_path)
    
    # 删除包含缺失值的行
    df = df.dropna(subset=['Greening rate', 'Property management fee（/m²/month USD）'])

    # 检查是否存在 'Building type' 列
    if 'Building type' in df.columns:
        # 获取唯一的建筑类型
        unique_types = df['Building type'].unique()
        
        # 创建映射字典
        type_mapping = {building_type: idx + 1 for idx, building_type in enumerate(unique_types)}
        
        # 替换 'Building type' 列中的值
        df['Building type'] = df['Building type'].map(type_mapping)
        
        # 保存更新后的 DataFrame
        df.to_excel(file_path, index=False)
        print(f"已处理文件: {file_path}")
    else:
        print(f"文件 {file_path} 中没有 'Building type' 列。")

# 主程序
directory_path = "C:/Users/Herzog/Desktop/2025美赛/数据/城市2"
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        process_file(file_path)

print("所有文件处理完成。") 