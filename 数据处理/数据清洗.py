import pandas as pd

def clean_data(file_path):
    # 读取数据文件，指定编码
    df = pd.read_excel(file_path)  # 使用 read_excel 读取 Excel 文件

    # 数据清洗
    # 1. 去除重复行（只考虑除了 Community Number 以外的其他列）
    df.drop_duplicates(subset=df.columns.difference(['Community Number']), inplace=True)

    # 2. 去除缺失值
    df.dropna(inplace=True)

    # 输出清洗后的数据到新路径
    output_file_path = file_path.replace('.xlsx', '_cleaned.xlsx')  # 添加后缀以区分
    df.to_excel(output_file_path, index=False)  # 使用 to_excel 输出 Excel 文件

# 示例用法
clean_data("C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 1_城市1待 售 房 产 的 基 本 信 息.xlsx")