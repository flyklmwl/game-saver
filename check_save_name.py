import os
import re
import json

dirdict = os.listdir("e:\Playnite919\save_gui\savedata")
saves_count = 0
dir_count = 0

for dir in dirdict:
    dir_count += 1
    with open(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", "r", encoding='utf-8') as json_file:
        save_dict = json.load(json_file)
        saves = save_dict["saves"]
        title = save_dict["title"]
        for save in saves:
            saves_count += 1
            path = save['path']
            # 查找存档记录的游戏名，并比对title名是否一致
            save_dir = re.search("\./savedata\/(.*)\/.*", path)
            # 预处理括号
            savename = re.sub(r"\(", r"\(", save_dir.group(1))
            savename = re.sub(r"\)", r"\)", savename)
            print(path)
            # 替换
            save["path"] = re.sub(savename, dir, path)
    # 写入存档配置文件
    # os.rename(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json.bak")
    # with open(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", "w+", encoding='utf-8') as dump_file:
    #     json.dump(save_dict, dump_file, ensure_ascii=False)
    # print("配置写入成功！")

print(f"游戏数量: {dir_count}")
print(f"游戏存档数: {saves_count}")
