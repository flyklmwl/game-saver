import os
import json
import time
import argparse
import py7zr
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
import shutil


class SaveGui(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        # 程序变量
        self.backuptime = ""
        self.save_env = f"./savedata/{gamename}/Saves.json"
        self.gamedir_var = ttk.StringVar(value=gamedir)
        self.save_desc = ttk.StringVar(value="")
        self.save_name = f"SaveFile_{self.backuptime}.7z"
        self.save_path = f"./savedata/{gamename}/{self.save_name}"

        self._init_env()
        self.pack(fill=BOTH, expand=YES)

        # 第一行容器的标题设置和位置选项配置，option_lf是带标题的行容器
        option_text = "游戏存档备份"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        # 加载目录行
        self.create_backup_row()
        self.create_backup2_row()
        self.create_manager_row()
        self.create_results_view()

    def _init_env(self):
        # 创建备份文件夹
        try:
            os.makedirs(f"./savedata/{gamename}")
        except FileExistsError:
            print("文件夹已存在！")
        # 写入配置文件
        if os.path.exists(self.save_env):
            pass
        else:
            save_dict = {
                "title": gamename,
                "saves": [],
            }
            with open(self.save_env, "w+", encoding='utf-8') as f:
                json.dump(save_dict, f, ensure_ascii=False)
            print("加载入文件完成...")
        self._check_save_file()

    def create_backup_row(self):
        """游戏存档备份"""
        backup_row = ttk.Frame(self.option_lf)
        backup_row.pack(fill=X, expand=YES)
        backup_lbl = ttk.Label(backup_row, text="备份目录", width=8)
        backup_lbl.pack(side=LEFT, padx=(15, 0))
        backup_ent = ttk.Entry(backup_row, textvariable=self.gamedir_var)
        backup_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=backup_row,
            text="查询存档",
            command=self.show_saves,
            bootstyle=INFO,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_backup2_row(self):
        backup_row2 = ttk.Frame(self.option_lf)
        backup_row2.pack(fill=X, expand=YES, pady=15)
        backup_lbl2 = ttk.Label(backup_row2, text="描述信息", width=8)
        backup_lbl2.pack(side=LEFT, padx=(15, 0))
        backup_ent2 = ttk.Entry(backup_row2, textvariable=self.save_desc)
        backup_ent2.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=backup_row2,
            text="备份存档",
            command=self.on_save,
            bootstyle=SUCCESS,
            width=8,
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_manager_row(self):
        backup_row3 = ttk.Frame(self.option_lf)
        backup_row3.pack(fill=X, expand=YES, pady=15)
        browse_btn1 = ttk.Button(
            master=backup_row3,
            text="存档目录",
            command=lambda: os.startfile(gamedir),
            width=8,
            bootstyle=INFO,
        )
        browse_btn1.pack(side=LEFT, padx=15)
        browse_btn2 = ttk.Button(
            master=backup_row3,
            text="删除存档",
            command=self.on_delete,
            width=8,
            bootstyle=DANGER,
        )
        browse_btn2.pack(side=LEFT, padx=15)
        browse_btn3 = ttk.Button(
            master=backup_row3,
            text="恢复存档",
            command=self.on_restore,
            width=8,
            bootstyle=SUCCESS,
        )
        browse_btn3.pack(side=LEFT, padx=15)

    def create_results_view(self):
        """Add result treeview to labelframe 添加图形结果"""
        self.resultview = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0, 1, 2, 3],
            show=HEADINGS
        )
        self.resultview.pack(fill=BOTH, expand=YES, pady=10)

        # setup columns and use `scale_size` to adjust for resolution
        self.resultview.heading(0, text='名称', anchor=W)
        self.resultview.heading(1, text='描述', anchor=W)
        self.resultview.heading(2, text='位置', anchor=E)
        self.resultview.heading(3, text='大小', anchor=E)
        self.resultview.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 200),
            stretch=False
        )
        self.resultview.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 350),
            stretch=False
        )
        self.resultview.column(
            column=2,
            anchor=E,
            width=utility.scale_size(self, 200),
            stretch=False
        )
        self.resultview.column(
            column=3,
            anchor=E,
            width=utility.scale_size(self, 50),
            stretch=False
        )

    def on_save(self):
        """备份 目录"""
        self.backuptime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        self.save_name = f"SaveFile_{self.backuptime}.7z"
        self.save_path = f"./savedata/{gamename}/{self.save_name}"
        # 备份参数
        srcdir = self.gamedir_var.get()
        # 备份开始
        with py7zr.SevenZipFile(self.save_path, 'w') as archive:
            archive.writeall(srcdir, self.save_name[:-3])
        os.path.getsize(self.save_path)
        print("备份完成")
        # 加载配置文件
        with open(self.save_env, 'r', encoding='utf-8') as load_f:
            save_dict = json.load(load_f)
        # 写入配置文件
        save_dict['saves'].append(
            {
                "name": self.save_name,
                "date": self.backuptime,
                "describe": self.save_desc.get(),
                "path": self.save_path,
                "size": self._formatsize(os.path.getsize(self.save_path))
            }
        )
        with open(self.save_env, "w+", encoding='utf-8') as f:
            json.dump(save_dict, f, ensure_ascii=False)
        print("写入配置文件完成...")
        self.show_saves()

    def on_delete(self):
        selected = self.resultview.focus()
        # values 拿到的是一个列表，只能按顺序取值
        values = self.resultview.item(selected)["values"]
        save_path = values[2]
        os.remove(save_path)
        with open(self.save_env, 'r', encoding='utf-8') as load_f:
            save_dict = json.load(load_f)
            saves = save_dict['saves']
        saves = [save for save in saves if save['path'] != save_path]
        save_dict['saves'] = saves
        # 写入配置文件
        with open(self.save_env, "w+", encoding='utf-8') as f:
            json.dump(save_dict, f, ensure_ascii=False)
        self.show_saves()
        print("删除存档完成!")

    def on_restore(self):
        # 获取要恢复的存档文件路径
        selected = self.resultview.focus()
        values = self.resultview.item(selected)["values"]
        save_path = values[2]
        # 恢复目录
        os.rename(gamedir, f"{gamedir}({round(time.time())})")
        with py7zr.SevenZipFile(save_path, 'r') as archive:
            archive.extractall(f"./savedata/{gamename}/")
        shutil.move(save_path[:-3], gamedir)
        print("恢复存档完成!!!")

    def show_saves(self):
        for i in self.resultview.get_children():
            self.resultview.delete(i)
        with open(self.save_env, "r", encoding='utf-8') as load_f:
            saves_info = json.load(load_f)
        # print(saves_info)
        for save_info in saves_info['saves']:
            save_name = save_info['name']
            save_desc = save_info['describe']
            save_path = save_info['path']
            save_size = save_info['size']
            self.resultview.insert(
                parent='',
                index=END,
                values=(save_name, save_desc, save_path, save_size)
            )

    def _check_save_file(self):
        # todo 检查配置文件中的存档是否存在
        pass

    @staticmethod
    def _formatsize(filesize):
        try:
            _bytes = float(filesize)    # 默认字节
            kb = _bytes / 1024          # 换算KB
        except:
            print("字节格式有误")
            return "Error"
        if kb >= 1024:
            m = kb / 1024               # KB换成M
            if m >= 1024:
                g = m / 1024
                return f"{round(g, 2)}G"
            else:
                return f"{round(m, 2)}M"
        else:
            return f"{round(kb, 2)}kb"


if __name__ == '__main__':
    # 设置命令行参数用来接收备份参数
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--game_name", help="timer name")
    parser.add_argument("-d", "--directory", help="project name")
    args = parser.parse_args()
    gamedir = args.directory
    gamename = args.game_name
    # 启动界面
    app = ttk.Window(gamename, "journal")
    # app.geometry('800x500')
    app.resizable(height=False, width=False)
    SaveGui(app)
    app.mainloop()
