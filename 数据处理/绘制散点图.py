import pandas as pd
import matplotlib.pyplot as plt
import os
import re  # 用于正则表达式处理

def plot_data(file_path, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 设置字体以支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 读取数据文件
    df = pd.read_excel(file_path)  # 使用 read_excel 读取 Excel 文件

    # 确保 Price (USD) 列为数值类型
    df['Price (USD)'] = pd.to_numeric(df['Price (USD)'], errors='coerce')

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

    # 为每个 Y 轴列绘制单独的散点图
    for column in y_columns:
        if column in df.columns:  # 确保列存在
            # 确保 Y 轴列为数值类型
            df[column] = pd.to_numeric(df[column], errors='coerce')

            plt.figure(figsize=(12, 6))
            plt.scatter(df['Price (USD)'], df[column], label=column, alpha=0.6)
            plt.title(f'价格与{translation_dict[column]}的关系')
            plt.xlabel('价格 (USD)')
            plt.ylabel(translation_dict[column])
            plt.legend()
            plt.grid()

            # 清理文件名，替换非法字符
            safe_column_name = re.sub(r'[<>:"/\\|?*]', '_', translation_dict[column])
            output_file_path = os.path.join(output_dir, f'价格_vs_{safe_column_name}.png')
            plt.savefig(output_file_path)
            plt.close()  # 关闭图形以释放内存

# 示例用法
output_directory = "C:/Users/Herzog/Desktop/2025美赛/图表/城市1图"
plot_data("C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 1_城市1待 售 房 产 的 基 本 信 息.xlsx", output_directory)