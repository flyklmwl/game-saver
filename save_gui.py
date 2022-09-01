import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SaveGui(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        # 程序变量
        self.path_var = ttk.StringVar(value=gamedir)

        # 第一行容器的标题设置和位置选项配置，option_lf是带标题的行容器
        option_text = "游戏存档管理"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        # 加载目录行
        self.create_path_row()

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="备份目录", width=8)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=path_row,
            text="备份存档",
            command=self.on_save,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def on_save(self):
        """备份 目录"""
        srcdir = self.path_var.get()
        print(f"从{srcdir}拷贝到destdir")
        print("备份完成")


if __name__ == '__main__':
    gamedir = sys.argv[1]
    app = ttk.Window("Save Gui", "journal")
    SaveGui(app)
    app.mainloop()
