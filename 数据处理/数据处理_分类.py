import pandas as pd
import os  # 导入 os 模块


def replace_building_types(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件未找到: {file_path}")
        return

    # 读取数据表格
    df = pd.read_excel(file_path)  # 修改为读取 Excel 文件

    # 获取建筑类型列
    building_types = df['Building type'].unique()

    # 创建一个映射字典，将建筑类型映射到整数编号
    type_mapping = {building_type: idx + 1 for idx, building_type in enumerate(building_types)}

    # 替换建筑类型为整数编号
    df['Building type'] = df['Building type'].map(type_mapping)

    # 输出替换好的数据
    output_file_path = "C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix_2_modified.xlsx"  # 新文件名
    df.to_excel(output_file_path, index=False)  # 修改为输出新的 Excel 文件


# 调用函数示例
replace_building_types(
    "C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 2_城市2待 售 房 产 的 基 本 信 息.xlsx")  # 确保路径正确