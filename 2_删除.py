import pandas as pd
import os


def clean_and_save_data(input_path, output_path=None):
    """
    清理输入的xlsx或csv文件数据:
    - 删除含有缺失值的数据行
    - 删除重复的数据行
    - 打印原始数据尺寸、删除的缺失值和重复值的数量
    - 保存清理后的数据到新的文件

    参数:
    - input_path: 输入文件路径 (.xlsx或.csv)
    - output_path: 输出文件路径 (默认在输入路径同一目录下保存为cleaned_ + 输入文件名)

    返回:
    - 保存成功或失败的状态信息
    """

    # 获取文件扩展名
    input_file, input_extension = os.path.splitext(input_path)
    input_file = os.path.basename(input_file)  # 获取输入文件名部分

    try:
        # 读取数据
        if input_extension.lower() == '.xlsx':
            df = pd.read_excel(input_path)
        elif input_extension.lower() == '.csv':
            df = pd.read_csv(input_path)
        else:
            print(f"文件格式 {input_extension} 不支持。仅支持.xlsx或.csv文件。")
            return False

        # 打印原始数据尺寸
        original_rows, original_cols = df.shape
        print(f"原始数据尺寸: {original_rows} 行, {original_cols} 列")

        # 删除缺失值
        df_cleaned = df.dropna()
        rows_after_missing = df_cleaned.shape[0]
        missing_rows_dropped = original_rows - rows_after_missing
        print(f"删除了 {missing_rows_dropped} 条缺失值数据")

        # 删除重复值
        df_cleaned = df_cleaned.drop_duplicates()
        rows_after_duplicates = df_cleaned.shape[0]
        duplicate_rows_dropped = rows_after_missing - rows_after_duplicates
        print(f"删除了 {duplicate_rows_dropped} 条重复数据")

        # 打印清理后的数据尺寸
        print(f"清理后的数据尺寸: {rows_after_duplicates} 行, {original_cols} 列")

        # 生成输出文件路径
        if output_path is None:
            output_file = f"cleaned_{input_file.lower()}" + input_extension.lower()
            output_path = os.path.join(os.path.dirname(input_path), output_file)
        else:
            # 确保输出路径的扩展名与输入一致
            output_path, output_ext = os.path.splitext(output_path)
            output_path += input_extension

        # 保存数据
        if input_extension.lower() == '.xlsx':
            df_cleaned.to_excel(output_path, index=False)
        elif input_extension.lower() == '.csv':
            df_cleaned.to_csv(output_path, index=False)

        print(f"数据已成功保存到: {output_path}")
        return True

    except FileNotFoundError:
        print(f"文件 {input_path} 不存在。")
        return False


# 测试函数
if __name__ == "__main__":
    input_path = "test1.xlsx"  # 替换为你的文件路径
    result = clean_and_save_data(input_path)
    if result:
        print("文件处理完成！")
    else:
        print("文件处理失败，请检查路径或文件格式。")