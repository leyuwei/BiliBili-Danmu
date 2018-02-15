#! -*- coding:utf-8 -*-

"""
Author:LeYuwei
2018.02.13
"""

import os
import re
import requests
import random

host = "http://comment.bilibili.com/"
suffix = ".xml"
global av

Agents = (
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
)

def getAv():
    while True:
        try:
            av = input("请输入AV号(如：19499330） :")
            url = "http://www.bilibili.com/video/av" + str(av) + "/"
            getHTMLText(url, av)
        except:
            print("输入错误，请检查您的输入！")


def getHTMLText(url, av):
    headers = {
        'User-Agent': random.choice(Agents)
    }
    u = requests.get(url=url, headers=headers)
    html = u.text
    cidlist = re.findall(r'cid=(.*?)&aid=', html)
    if len(cidlist)==0:
        regex = re.compile(r',\"cid\":(\d*)')
        cidlist = regex.findall(html)
        cidlist.remove(cidlist[0])
        print("自识别为分P的视频...")
        countt = 0
        for cid in cidlist:
            print("正在获取Episode... ",str(countt+1))
            countt += 1
            getDanmu(int(cid),av,isMultipleEpisode=True,epi=countt)
    else:
        cid = int(cidlist[0])
        print("已获取弹幕地址...")
        getDanmu(cid, av)


def getDanmu(cid, av, isMultipleEpisode=False, epi=0):
    dmurl = "http://comment.bilibili.com/" + str(cid) + ".xml"
    dmhtml = requests.get(dmurl).text
    print("获得弹幕，开始处理...")
    dr = re.compile(r'<[^>]+>', re.S)
    dmlistcontent = dr.sub('\n', dmhtml)
    dmlist = dmlistcontent.split('\n')
    while "" in dmlist:
        dmlist.remove("")
    for ind in range(7):
        del dmlist[0]
    print("弹幕处理完成，准备存入文件...")
    printDanmu(dmlist, av, isMultipleEpisode=isMultipleEpisode, epi=epi)


def printDanmu(dmlist, av, isMultipleEpisode=False, epi=0):
    if isMultipleEpisode==False:
        filename = "av" + str(av) + ".txt"
        print("正在写入txt文件...")
        with open(filename, 'w', encoding='utf-8') as t:
            for dm in dmlist:
                t.write(dm + '\n')
        print("写入txt文件完成！")
    else:
        cur_path = os.path.abspath(os.curdir)
        path = cur_path + "\\av" + av
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path + "\\episode_" + str(epi) + ".txt"
        print("正在写入分P弹幕文件...")
        with open(filename, 'w', encoding='utf-8') as t:
            for dm in dmlist:
                t.write(dm + '\n')
        print("写入分P弹幕文件完成！")


if __name__ == "__main__":
    getAv()