import requests
import argparse
from tqdm import tqdm
from zipfile import ZipFile
from datetime import datetime
import os


def download(download_file):
    print("开始从阿里云下载游戏")
    print(aliyun_download_url)
    response = requests.get(aliyun_download_url, stream=True)  # 设stream流传输方式为真
    if response.headers["Server"] != "AliyunOSS":
        print("开始从百度下载游戏")
        headers = {
            "User-Agent": "pan.baidu.com"
        }
        response = requests.get(baidu_download_url, headers=headers, stream=True)  # 设stream流传输方式为真

    # print(response.headers)               # 打印查看基本头信息
    data_size = int(response.headers['Content-Length'])/1024/1024                   # 字节/1024/1024=MB
    # print(data_size/100)
    with open(rf'{download_file}', 'wb') as f:
        for data in tqdm(iterable=response.iter_content(1024*1024), total=round(data_size), desc='正在下载', unit='MB'):
            f.write(data)


if __name__ == '__main__':
    # 接收变量
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game_dbid", help="game db id")
    parser.add_argument("-d", "--PlayniteDir", help="Playnite dir")
    args = parser.parse_args()
    # 加工变量
    gamedbid = args.game_dbid
    playnitedir = args.PlayniteDir
    download_temp_dir = rf"{playnitedir}\..\Playnite_Games\temp"
    download_file = rf"{download_temp_dir}\{gamedbid}.zip"
    gamesource_dir = rf"{playnitedir}\..\Playnite_Games\PC"
    # aliyun_url = "http://alist.windcs.cn/d/gamedir_source/PC"
    aliyun_url = "http://alist.windcs.cn/d/aliyun/gamedir_source/PC"
    baidu_url = "http://alist.windcs.cn/d/baidu/gamedir_source/PC"
    aliyun_download_url = f"{aliyun_url}/{gamedbid}.zip"
    baidu_download_url = f"{baidu_url}/{gamedbid}.zip"
    game_dir = rf"{gamesource_dir}\{gamedbid}"

    # 判断是否存在游戏目录
    if os.path.exists(game_dir):
        print("游戏已经安装")
        os.system("pause")
        exit(-1)
    # 下载到temp目录
    try:
        download(download_file)
    except FileNotFoundError:
        os.makedirs(download_temp_dir)
        download(download_file)
    # 解压到gamedir
    start_time = datetime.now()
    with ZipFile(file=download_file) as zip_file:
        for file in tqdm(iterable=zip_file.namelist(), total=len(zip_file.namelist())):
            try:
                zip_file.extract(member=file, path=gamesource_dir)
            except:
                zip_file.extract(member=file, path=gamesource_dir, pwd="Flykl3321*")

    # 解压完成后处理乱码
    for root, dirs, files in os.walk(game_dir):
        for d in dirs:
            try:
                new_dname = d.encode('cp437').decode('gbk')
                os.rename(os.path.join(root, d), os.path.join(root, new_dname))
            except:
                new_dname = d.encode('cp437').decode('utf-8')
                os.rename(os.path.join(root, d), os.path.join(root, new_dname))
    for root, dirs, files in os.walk(game_dir):
        for f in files:
            try:
                new_name = f.encode('cp437').decode('gbk')
                os.rename(os.path.join(root, f), os.path.join(root, new_name))
            except:
                new_name = f.encode('cp437').decode('utf-8')
                os.rename(os.path.join(root, f), os.path.join(root, new_name))
    end_time = datetime.now()
    use_time = end_time - start_time
    print(f"Usetime is {use_time}")
    os.remove(download_file)
    print("游戏已安装完毕")
    os.system("pause")
