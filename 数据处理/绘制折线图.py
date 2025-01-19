import pandas as pd
import matplotlib.pyplot as plt

def plot_data(file_path):
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

    # 为每个 Y 轴列绘制单独的折线图
    for column in y_columns:
        if column in df.columns:  # 确保列存在
            # 确保 Y 轴列为数值类型
            df[column] = pd.to_numeric(df[column], errors='coerce')

            plt.figure(figsize=(12, 6))
            plt.plot(df['Price (USD)'], df[column], label=column)
            plt.title(f'Price vs {column}')
            plt.xlabel('Price (USD)')
            plt.ylabel(column)
            plt.legend()
            plt.grid()
            plt.show()

# 示例用法
plot_data("C:/Users/Herzog/Desktop/2025美赛/题目/2024_“ShuWei Cup”D_Problem/Appendix 1_城市1待 售 房 产 的 基 本 信 息.xlsx") 