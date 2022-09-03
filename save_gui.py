import os
import json
import time
import argparse
import py7zr
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import shutil


class SaveGui(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)
        self.backuptime = ""
        self.write_json()

        # 程序变量
        self.gamedir_var = ttk.StringVar(value=gamedir)
        self.savedesc = ttk.StringVar(value="")

        # 第一行容器的标题设置和位置选项配置，option_lf是带标题的行容器
        option_text = "游戏存档备份"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        # 加载目录行
        self.create_backup_row()
        self.create_backup2_row()

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
            text="备份存档",
            command=self.on_save,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def create_backup2_row(self):
        backup_row2 = ttk.Frame(self.option_lf)
        backup_row2.pack(fill=X, expand=YES, pady=15)
        backup_lbl2 = ttk.Label(backup_row2, text="描述信息", width=8)
        backup_lbl2.pack(side=LEFT, padx=(15, 0))
        backup_ent2 = ttk.Entry(backup_row2, textvariable=self.savedesc)
        backup_ent2.pack(side=LEFT, fill=X, expand=YES, padx=5)

    def on_save(self):
        """备份 目录"""
        self.backuptime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        _7zfile = f"SaveFile_{self.backuptime}.7z"
        save_path = f"./savedata/{gamename}/{_7zfile}"
        # 备份参数
        srcdir = self.gamedir_var.get()
        # 备份开始
        with py7zr.SevenZipFile(save_path, 'w') as archive:
            archive.writeall(srcdir, "savefile")
        print(f"从{srcdir}拷贝到destdir")
        print("备份完成")
        # 加载配置文件
        with open(f"./savedata/{gamename}/Saves.json", 'r', encoding='utf-8') as load_f:
            save_dict = json.load(load_f)
        # 写入配置文件
        save_dict['saves'].append(
            {
                "date": self.backuptime,
                "describe": self.savedesc.get(),
                "path": save_path,
            }
        )
        with open(f"./savedata/{gamename}/Saves.json", "w+", encoding='utf-8') as f:
            json.dump(save_dict, f, ensure_ascii=False)
        print("加载入文件完成...")

        # with open(f"E:\游戏存档管理-0.3.0-win\save_data\缺氧/Saves.json", 'r', encoding='utf-8') as load_f:
        #      save_dict = json.load(load_f)
        # print(save_dict)

    def write_json(self):
        # 变量定义
        save_env = f"./savedata/{gamename}/Saves.json"
        # 创建备份文件夹
        try:
            os.makedirs(f"./savedata/{gamename}")
        except FileExistsError:
            print("文件夹已存在！")
        # 写入配置文件
        if os.path.exists(save_env):
            pass
        else:
            save_dict = {
                "name": gamename,
                "saves": [],
            }
            with open(save_env, "w+", encoding='utf-8') as f:
                json.dump(save_dict, f, ensure_ascii=False)
            print("加载入文件完成...")
        self._check_save_file()

    def _check_save_file(self):
        # todo 检查配置文件中的存档是否存在
        pass


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
    app.geometry('800x600')
    SaveGui(app)
    app.mainloop()
