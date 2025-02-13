# 标准化（Z - score normalization）
# 最小 - 最大标准化（Min - Max scaling）
# Box - Cox 变换
# 中心化对数比变换
import pandas as pd
import numpy as np
from scipy.stats import zscore, boxcox
from sklearn.preprocessing import MinMaxScaler
import os


def read_file(file_path):
    """读取文件（支持 .csv, .xls, .xlsx）"""
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件路径不存在！")

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    else:
        raise ValueError("不支持的文件格式！仅支持 .csv, .xls 和 .xlsx 文件。")


def select_columns(data):
    """让用户选择需要变换的列"""
    print("以下为数据的列名：")
    for idx, column in enumerate(data.columns):
        print(f"{idx}. {column}")

    selected_columns = input("请输入需要进行变换的列索引（用逗号分隔）：").split(',')
    selected_columns = [col.strip() for col in selected_columns]

    columns = []
    for col in selected_columns:
        if col.isdigit():
            index = int(col)
            if 0 <= index < len(data.columns):
                columns.append(data.columns[index])
            else:
                raise ValueError(f"列索引 {col} 超出范围！")
        else:
            if col in data.columns:
                columns.append(col)
            else:
                raise ValueError(f"列名 '{col}' 不存在！")

    if not columns:
        raise ValueError("未选择任何列！")

    return columns


def select_transformation():
    """让用户选择变换方法"""
    print("请选择需要使用的变换方法：")
    print("1. Z-score 标准化")
    print("2. Min-Max 标准化")
    print("3. Box-Cox 变换")
    print("4. 中心化对数比变换")

    transformation = input("请输入数字选择（1-4）：")
    if not transformation.isdigit():
        raise ValueError("请输入数字！")

    transformation = int(transformation)
    if transformation < 1 or transformation > 4:
        raise ValueError("请输入 1-4 之间的数字！")

    return transformation


def apply_zscore(data, columns):
    """应用 Z-score 标准化"""
    for column in columns:
        data[column] = zscore(data[column])
    return data


def apply_minmax(data, columns):
    """应用 Min-Max 标准化"""
    scaler = MinMaxScaler()
    for column in columns:
        data[column] = scaler.fit_transform(data[[column]])
    return data


def apply_boxcox(data, columns):
    """应用 Box-Cox 变换"""
    for column in columns:
        transformed, _ = boxcox(data[column] + 1)  # 避免零值
        data[column] = transformed
    return data


def apply_clr(data, columns):
    """应用中心化对数比变换"""
    log_data = np.log(data[columns].values + 1e-10)  # 防止零值
    clr = log_data - log_data.mean(axis=1, keepdims=True)
    data[columns] = clr
    return data


def transform_data(data, columns, method):
    """根据选择的方法进行数据变换"""
    if method == 1:
        return apply_zscore(data, columns)
    elif method == 2:
        return apply_minmax(data, columns)
    elif method == 3:
        return apply_boxcox(data, columns)
    elif method == 4:
        return apply_clr(data, columns)
    else:
        raise ValueError("未知的变换方法！")


def save_data(data, output_path):
    """保存处理后的数据"""
    _, file_extension = os.path.splitext(output_path)
    file_extension = file_extension.lower()

    if file_extension == '.csv':
        data.to_csv(output_path, index=False)
    elif file_extension in ['.xls', '.xlsx']:
        data.to_excel(output_path, index=False)
    else:
        raise ValueError("不支持的文件格式！仅支持 .csv, .xls 和 .xlsx 文件。")


def main():
    try:
        # 输入文件路径
        file_path = input("请输入数据文件路径（.xlsx 或 .csv）：")
        data = read_file(file_path)

        # 选择变换方法
        method = select_transformation()

        # 选择列
        columns = select_columns(data)

        # 应用变换
        print("正在应用变换...")
        data_transformed = transform_data(data.copy(), columns, method)
        print("变换完成！")

        # 输出文件路径
        output_path = input("请输入保存结果的文件路径（默认与输入路径相同，替换文件后缀为 _transformed）：")
        if not output_path:
            original_path, ext = os.path.splitext(file_path)
            output_path = f"{original_path}_transformed{ext}"

        save_data(data_transformed, output_path)
        print(f"数据预处理完成！结果已保存至：{output_path}")

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()


