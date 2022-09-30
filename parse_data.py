import json

with open('data/Game.json', 'r') as json_file:
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

with open("data/Game1.json", "w+", encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False)

print(i)
