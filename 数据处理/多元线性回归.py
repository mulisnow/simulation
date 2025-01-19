import pandas as pd
import os
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 读取区域数据
area_data = {
    '区域': ['赛罕区', '新城区', '土默特左旗', '回民县', '玉泉区', '和林格尔县', '托克托县', '武川县', '清水河区'],
    '2022年总人数': [597178, 464230, 354384, 243915, 219608, 201939, 196473, 162978, 136372],
    '人均GDP（万元/人）': [12.39, 10.54, 8.76, 9.28, 7.44, 20.95, 14.01, 7.08, 11.69]
}
area_df = pd.DataFrame(area_data)

# 主程序
directory_path = "C:/Users/Herzog/Desktop/2025美赛/数据/城市2"
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory_path, filename)
        df = pd.read_excel(file_path)

        # 获取文件名作为区域名
        region_name = filename[:-5]  # 去掉文件扩展名

        # 查找对应区域的数据
        region_data = area_df[area_df['区域'] == region_name]
        if not region_data.empty:
            # 合并数据
            merged_df = df.merge(region_data, left_on='Class', right_on='区域', how='left')

            # 检查合并后的数据
            print(f"合并后的数据 (区域: {region_name}):")
            print(merged_df)

            # 检查是否有足够的数据
            if not merged_df.empty:
                # 选择自变量和因变量
                X = merged_df[['Greening rate', 'Property management fee（/m²/month USD）', '2022年总人数', '人均GDP（万元/人）']]
                y = merged_df['Price (USD)']

                # 转换数据类型
                X = X.apply(pd.to_numeric, errors='coerce')
                y = pd.to_numeric(y, errors='coerce')

                # 删除包含 NaN 的行
                X = X.dropna()
                y = y[X.index]  # 确保 y 也只包含对应的索引

                # 检查是否有足够的数据进行回归
                if len(y) > 0 and len(X) > 0:
                    # 添加常数项
                    X = sm.add_constant(X)

                    # 进行多元线性回归
                    model = sm.OLS(y, X).fit()

                    # 获取回归系数
                    coefficients = model.params
                    equation = f"y = {coefficients[0]:.4f} + "
                    equation += " + ".join([f"{coefficients[i]:.4f}*{X.columns[i-1]}" for i in range(1, len(coefficients))])

                    # 计算 VIF
                    vif_data = pd.DataFrame()
                    vif_data["feature"] = X.columns
                    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

                    # 输出 VIF
                    print(f"区域: {region_name} 的 VIF 数据:")
                    print(vif_data)

                    # 保存结果
                    output_path = os.path.join(directory_path, f"{region_name}方程.txt")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(equation)
                    print(f"区域: {region_name} 的回归方程已保存到: {output_path}")
                else:
                    print(f"区域: {region_name} 没有足够的数据进行回归。")
            else:
                print(f"区域: {region_name} 没有足够的数据进行回归。")
        else:
            print(f"文件 {filename} 中的区域名 {region_name} 未找到。")

print("所有文件处理完成。") 