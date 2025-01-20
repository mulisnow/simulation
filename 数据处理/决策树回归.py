import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib

# 设置字体以支持中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 主程序
directory_path = "C:/Users/Herzog/Desktop/2025美赛/数据/城市2"
output_directory = "C:/Users/Herzog/Desktop/2025美赛/图表/回归结果"

# 确保输出目录存在
os.makedirs(output_directory, exist_ok=True)

for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        df = pd.read_excel(file_path)

        # 打印 DataFrame 的内容和数据类型以检查
        print(f"文件: {filename} 的数据:\n{df.head()}")
        print(f"文件: {filename} 的数据类型:\n{df.dtypes}")

        # 选择自变量和因变量，移除不需要的列
        try:
            X = df[['Total number of households', 'Greening rate', 'Floor area ratio', 
                     'Building type', 
                     'Property management fee（/m²/month USD）']]  # 移除不需要的列
            y = df['Price (USD)']
        except KeyError as e:
            print(f"文件 {filename} 中缺少必要的列: {e}")
            continue

        # 转换数据类型
        X.loc[:, 'Property management fee（/m²/month USD）'] = pd.to_numeric(X['Property management fee（/m²/month USD）'], errors='coerce')

        # 检查缺失值
        print(f"文件: {filename} 的缺失值情况:\n{df.isnull().sum()}")

        # 填充缺失值（可以选择均值填充或其他方法）
        X.fillna(X.mean(), inplace=True)
        y.fillna(y.mean(), inplace=True)

        # 删除包含 NaN 的行
        X = X.dropna()
        y = y[X.index]  # 确保 y 也只包含对应的索引

        # 输出调试信息
        print(f"X 的形状: {X.shape}, y 的形状: {y.shape}")

        # 检查是否有足够的数据进行回归
        if len(y) > 0 and len(X) > 0:
            # 决策树回归
            tree_model = DecisionTreeRegressor()
            tree_model.fit(X, y)
            y_pred_tree = tree_model.predict(X)

            # 计算性能指标
            mse = mean_squared_error(y, y_pred_tree)
            r2 = r2_score(y, y_pred_tree)

            # 输出结果
            print(f"决策树回归的均方误差 (MSE): {mse}")
            print(f"决策树回归的决定系数 (R²): {r2}")

            # 可视化结果
            plt.figure(figsize=(12, 8))
            plt.scatter(y, y_pred_tree, label='决策树回归', alpha=0.5)
            plt.xlabel('实际价格 (USD)')
            plt.ylabel('预测价格 (USD)')
            plt.title(f'{filename} 决策树回归预测结果')
            plt.legend()

            # 保存图表
            plot_filename = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_回归结果.png")
            plt.savefig(plot_filename)
            plt.close()  # 关闭图表以释放内存
            print(f"图表已保存到: {plot_filename}")

            # 保存结果
            output_path = os.path.join(directory_path, f"{filename}_决策树回归结果.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"决策树回归的均方误差 (MSE): {mse}\n")
                f.write(f"决策树回归的决定系数 (R²): {r2}\n")
            print(f"区域: {filename} 的决策树回归结果已保存到: {output_path}")
        else:
            print(f"区域: {filename} 没有足够的数据进行回归。")

print("所有文件处理完成。")