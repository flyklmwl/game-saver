import requests
import argparse
from tqdm import tqdm
import py7zr
import os


def download(download_url, download_file):
    url = download_url
    print(url)
    response = requests.get(url, stream=True)    # 设stream流传输方式为真
    # print(response.headers)               # 打印查看基本头信息
    data_size = int(response.headers['Content-Length'])/1024/1024                   # 字节/1024/1024=MB
    # print(data_size/100)
    with open(rf'{download_file}', 'wb') as f:
        for data in tqdm(iterable=response.iter_content(1024*1024), total=data_size, desc='正在下载', unit='MB'):
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
    download_temp_dir = rf"{playnitedir}\CustomGames(flyklmwl)\temp"
    download_file = rf"{download_temp_dir}\{gamedbid}.7z"
    gamesource_dir = rf"{playnitedir}\CustomGames(flyklmwl)\gamedir_source\PC"
    aliyun_url = "http://alist.windcs.cn/d/gamedir_source/PC"
    download_url = f"{aliyun_url}/{gamedbid}.7z"

    # 判断是否存在游戏目录
    if os.path.exists(rf"{gamesource_dir}\{gamedbid}"):
        print("游戏已经安装")
        os.system("pause")
        exit(-1)
    # 下载到temp目录
    download(download_url, download_file)
    # 解压到gamedir
    with py7zr.SevenZipFile(download_file, 'r') as archive:
        archive.extractall(gamesource_dir)
    os.remove(download_file)
    print("已安装完毕")
    os.system("pause")
