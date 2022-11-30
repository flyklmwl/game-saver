import json
import re
import os


def addnewoption():
    # 给命令行添加一个 -g 的参数
    with open('data/games.json', 'r') as json_file:
        items = json.load(json_file)

    # print(items)
    # print(type(items))
    i = 0
    for item in items:
        # 3bf32259-3807-4744-af53-03ee04945a8c
        try:
            for cateitem in item["CategoryIds"]:
                if cateitem['$guid'] == "3bf32259-3807-4744-af53-03ee04945a8c":
                    i += 1
                    # rint("属于备份存档分类", item['Name'], item['GameId'])
                    for action in item['GameActions']:
                        if action["Name"] == "备份存档":
                            arg = action["Arguments"]
                            action["Arguments"] = arg + " -g \"{DatabaseId}\""
                            print(action["Arguments"])
        except KeyError:
            continue

    with open("data/games_new.json", "w+", encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)

    print(i)


def modify_save_gui_path():
    with open('data/games.json', 'r') as json_file:
        items = json.load(json_file)
    modify_count = 0
    for item in items:
        # 把备份存档的路径替换
        # try:
        #     if item['GameActions']:
        #         for action in item['GameActions']:
        #             if action['Name'] == "备份存档":
        #                 modify_count += 1
        #                 # print(action['Path'])
        #                 if action['Path'] == "{PlayniteDir}\save_gui\save_gui.exe":
        #                     path = re.sub(r"\{PlayniteDir\}", r"{PlayniteDir}\\CustomGames(flyklmwl)", action['Path'])
        #                     action['Path'] = path
        #                     print(action['Path'])
        # except KeyError:
        #     pass
        try:
            # installdir = re.sub(r"\.\.\\Playnite_Games\\PC", r".\\CustomGames\(flyklmwl\)\\gamedir_source\\PC", item["InstallDirectory"])
            print(item["InstallDirectory"])
            modify_count += 1
        except KeyError:
            pass
    print(f"总计installdir有{modify_count}项")

    with open("data/games_new.json", "w+", encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)


def check_cloud_games():
    # GameId 是游戏id，并不是数据库id(_id才是)，游戏id是可能为空的
    game_list = []
    playnite_list = []
    playnite_list_id = []
    with open('data/games.json', 'r') as json_file:
        items = json.load(json_file)
    count = 0
    pc_games = os.listdir("e:\gamedir_source\PC")
    print(type(pc_games))
    for item in items:
        # if item['_id']["$guid"] == "afec845b-6c37-4cd9-87d3-e057e80d2777":
        #     print(f"符合id的游戏为: {item['Name']}")
        try:
            for cateitem in item["CategoryIds"]:
                # 3604de32-66b9-4af3-8363-e48b3a56d5a6 游戏云保存
                if cateitem['$guid'] == "3604de32-66b9-4af3-8363-e48b3a56d5a6":
                    count += 1
                    playnite_list.append(item["Name"])
                    playnite_list_id.append(item["_id"]["$guid"])
                    # print(item["_id"]["$guid"])
                    for name in pc_games:
                        pc_game_id = item["_id"]["$guid"]
                        pc_game = name[:-4]
                        if pc_game_id == pc_game:
                            # print(item["Name"])
                            game_list.append(item["Name"])
        except KeyError:
            continue
    print(count)
    print(len(game_list))
    print(len(playnite_list))

    diff_list = list(set(playnite_list) - set(game_list))
    print(f"pg: {diff_list}")

    # 对比百度上的
    baidu_list_id = []
    with open("data/baidu_list.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            line = line[:-4]
            line = line[49:]
            baidu_list_id.append(line)
    print(baidu_list_id)
    print(playnite_list_id)
    diff_list = list(set(baidu_list_id) - set(playnite_list_id))
    print(diff_list)


if __name__ == '__main__':
    # addnewoption()
    modify_save_gui_path()
    # check_cloud_games()
