import os
import re
import json

dirdict = os.listdir("e:\Playnite919\save_gui\savedata")
picdirs = os.listdir("e:\Playnite919\gamepic")
gamedict = []
saves_count = 0
dir_count = 0

for dir in dirdict:
    dir_count += 1
    with open(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", "r", encoding='utf-8') as json_file:
        save_dict = json.load(json_file)
        saves = save_dict["saves"]
        title = save_dict["title"]
        # 查询所有备份游戏名
        # print(title, dir)
        gamedict.append(
            {
                "title": title,
                "dir": dir
            }
        )
        # 处理目录是游戏名的问题
        # for save in saves:
        #     saves_count += 1
        #     path = save['path']
        #     # 查找存档记录的游戏名，并比对title名是否一致
        #     save_dir = re.search("\./savedata\/(.*)\/.*", path)
        #     # 预处理括号
        #     savename = re.sub(r"\(", r"\(", save_dir.group(1))
        #     savename = re.sub(r"\)", r"\)", savename)
        #     print(path)
        #     # 替换
        #     save["path"] = re.sub(savename, dir, path)
    # 写入存档配置文件
    # os.rename(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json.bak")
    # with open(f"e:\Playnite919\save_gui\savedata/{dir}/Saves.json", "w+", encoding='utf-8') as dump_file:
    #     json.dump(save_dict, dump_file, ensure_ascii=False)
    # print("配置写入成功！")

# 处理游戏截图文件夹
for picdir in picdirs:
    print(picdir)
    for game in gamedict:
        # print(game)
        if picdir == game['title']:
            print(f"{picdir}在标题对上了")
            os.rename(f"e:\Playnite919\gamepic\{picdir}", f"e:\Playnite919\gamepic\{game['dir']}")
            break
    #     else:
    #         break
    # print(f"{picdir}标题没有对上")


print(f"游戏数量: {dir_count}")
print(f"游戏存档数: {saves_count}")
