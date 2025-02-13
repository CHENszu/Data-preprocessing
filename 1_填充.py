import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def fill_missing_values(file_path):
    # 读取数据
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # 输出缺失值数量
    print("每列缺失值数量：")
    print(df.isnull().sum())
    print()

    # 处理缺失值
    df_filled = df.copy()

    for col in df.columns:
        if df[col].isnull().sum() > 0:
            # 如果有多列数据，使用随机森林回归填充
            if df.shape[1] > 1:
                # 准备训练数据和预测数据
                X_train = df[df[col].notnull()].drop(columns=col)
                y_train = df[df[col].notnull()][col]
                X_predict = df[df[col].isnull()].drop(columns=col)

                # 训练随机森林回归模型
                if not X_train.empty:
                    model = RandomForestRegressor(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)
                    # 预测缺失值
                    predicted = model.predict(X_predict)
                    # 将预测值填充到缺失列
                    df_filled.loc[df[col].isnull(), col] = predicted
                else:
                    # 如果训练数据为空，使用线性插值
                    df_filled[col] = df[col].interpolate(method='linear')
            else:
                # 只有一列，使用线性插值
                df_filled[col] = df[col].interpolate(method='linear')

    # 保存填充后的数据
    if file_path.endswith('.csv'):
        output_path = file_path.replace('.csv', '_filled.csv')
        df_filled.to_csv(output_path, index=False)
    else:
        output_path = file_path.replace('.xlsx', '_filled.xlsx')
        df_filled.to_excel(output_path, index=False)

    print(f"填充后的数据已保存到: {output_path}")


# 示例用法
fill_missing_values("test1.xlsx")  # 替换为你的文件路径