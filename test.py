import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd


class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV/Excel Viewer")
        self.root.geometry("800x600")

        # 创建界面组件
        self.create_widgets()
        self.df = None
        self.current_columns = []

    def create_widgets(self):
        # 顶部按钮区域
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_open = ttk.Button(self.top_frame, text="打开文件", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT)

        # 列选择区域
        self.left_frame = ttk.Frame(self.root, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.column_list = tk.Listbox(self.left_frame, selectmode=tk.MULTIPLE)
        self.column_list.pack(fill=tk.BOTH, expand=True)
        self.column_list.bind('<<ListboxSelect>>', self.update_columns)

        # 数据表格区域
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(self.tree_frame)
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel/CSV", "*.xlsx *.csv"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            else:
                self.df = pd.read_excel(file_path)

            self.update_column_list()
            self.update_table()
        except Exception as e:
            tk.messagebox.showerror("错误", f"无法读取文件:\n{str(e)}")

    def update_column_list(self):
        self.column_list.delete(0, tk.END)
        for col in self.df.columns:
            self.column_list.insert(tk.END, col)
        self.column_list.selection_set(0, tk.END)  # 默认全选

    def update_columns(self, event):
        selected = self.column_list.curselection()
        self.current_columns = [self.column_list.get(i) for i in selected]
        self.update_table()

    def update_table(self):
        # 清空现有表格
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = self.current_columns

        # 设置列标题和对齐方式
        for col in self.current_columns:
            # 居中对齐（新增anchor参数）
            self.tree.heading(col, text=col, anchor=tk.CENTER)  # 标题居中
            self.tree.column(col, width=150, anchor=tk.CENTER)  # 内容居中并加宽列

        # 添加数据行
        if self.df is not None and len(self.current_columns) > 0:
            for _, row in self.df[self.current_columns].iterrows():
                self.tree.insert("", tk.END, values=tuple(row))

        # 滚动到最左侧（新增这行）
        self.tree.xview_moveto(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataViewerApp(root)
    root.mainloop()