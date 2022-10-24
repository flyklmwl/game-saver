import json
import re


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
        try:
            if item['GameActions']:
                for action in item['GameActions']:
                    if action['Name'] == "备份存档":
                        modify_count += 1
                        # print(action['Path'])
                        if action['Path'] == "{PlayniteDir}\save_gui\save_gui.exe":
                            path = re.sub(r"\{PlayniteDir\}", r"{PlayniteDir}\\CustomGames(flyklmwl)", action['Path'])
                            action['Path'] = path
                            print(action['Path'])
        except KeyError:
            pass
    with open("data/games_new.json", "w+", encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)


if __name__ == '__main__':
    # addnewoption()
    modify_save_gui_path()
