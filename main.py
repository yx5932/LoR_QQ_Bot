#coding=utf-8
from email.mime import image
from glob import glob
from logging import exception
from pycqBot.cqApi import cqHttpApi, cqLog
from pycqBot.cqCode import at, image
from lor_deckcodes import LoRDeck, CardCodeAndCount

import json
import urllib
from unicodedata import name
from urllib.request import urlopen
import jsonpath
import pandas as pd
from langconv import *

cardcosts = []
cardcodes = []
cardnames = []
cardregions = []
cardtypes = []
cardsupertypes = []
cardrarities = []
cardengnames = []
costs = ['⓪','①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮','⑯','⑰','⑱','⑲','⑳']
sets_json = ''
champions = []
followers = []
spells = []
money = 0

with open("sets.json",'r',encoding='utf-8') as load_f:
    sets_json = json.load(load_f)
    cardcosts.extend(jsonpath.jsonpath(sets_json,'$..cost'))
    cardcodes.extend(jsonpath.jsonpath(sets_json,'$..cardCode'))
    cardnames.extend(jsonpath.jsonpath(sets_json,'$..name'))
    cardregions.extend(jsonpath.jsonpath(sets_json,'$..regions'))
    cardtypes.extend(jsonpath.jsonpath(sets_json,'$..type'))
    cardsupertypes.extend(jsonpath.jsonpath(sets_json,'$..supertype'))
    cardrarities.extend(jsonpath.jsonpath(sets_json,'$..rarity'))
    # cardengnames.extend(jsonpath.jsonpath(sets_json,'$..rarity'))
for i in range(len(cardnames)):
    cardnames[i] = Converter('zh-hans').convert(cardnames[i])
    
regions_code=['BC','BW','DE','FR','IO','MT','NX','PZ','SH','SI']
regions_name=['班德尔城','比尔吉沃特','德玛西亚','弗雷尔卓德','艾欧尼亚','巨神峰','诺克萨斯','皮祖','恕瑞玛','暗影岛']

def getinfo(cardinfo):
    cardcode = cardinfo[2:]
    cardnum = cardinfo[:1]
    # setinfo_html = urllib.request.urlopen(i)
    index = cardcodes.index(cardcode)
    rarity = cardrarities[index]
    global money
    if rarity=="英雄":
        money += 3000*int(cardnum)
    elif rarity=="史詩":
        money += 1200*int(cardnum)
    elif rarity=="稀有":
        money += 300*int(cardnum)
    elif rarity=="普通":
        money += 100*int(cardnum)
    info = ''
    if cardsupertypes[index] == "英雄":
        cost = cardcosts[index]
        info += '%s'%costs[cost]
        info += cardnames[index] + ' ' + cardnum + '张'
        champions.append(info)
    elif cardtypes[index] == "單位":
        cost = cardcosts[index]
        info += '%s'%costs[cost]
        info += cardnames[index] + ' ' + cardnum + '张'
        followers.append(info)
    elif cardtypes[index] == "法術":
        cost = cardcosts[index]
        info += '%s'%costs[cost]
        info += cardnames[index] + ' ' + cardnum + '张'
        spells.append(info)
        

# 启用日志 默认日志等级 DEBUG
cqLog()

cqapi = cqHttpApi()

# echo 函数
def echo(commandData, cqCodeList, message, from_id):
    # 发送群消息
    cqapi.send_group_msg(from_id, " ".join(commandData))

def 错误170000(commandData, cqCodeList, message, from_id):
    # 发送群消息
    text="如果账号地区没有问题（注册账号时如果没有开加速器，会导致账号归属地为中国（CHN），导致无法登陆游戏（错误代码1700000），检查账号所在地区攻略：账号地区检查），首次登陆游戏时也开了对应地区的加速器（首次登陆游戏时如果没有开账号对应地区的加速器，会被检测为账号归属地有误，从而导致黑号并无法登陆游戏），那就是网络问题网络问题网络问题，重要的事情说三遍。麻烦更换网络环境（开加速器的换节点，还是不行换个加速器；用有线网的改无线网；用无线网的换个别的无线网；WiFi不行就开流量；流量不行就换个运营商…）总而言之言而总之，更换网络环境。\r\r另外，自3.0版本以来，陆续有朋友在使用苹果设备的情况下，在试图更换账号时遇到170000问题，即使卸载游戏重装，也无法进入登陆界面。解决方法有如下2种：1、将设备格式化（恢复出厂设置），在格式化前请备份好自己的数据。 2、卸载LoR，然后更换其他地区的苹果账号再次下载。例如之前在美区苹果商店下载的LoR，可以切换成港区苹果账号再重新下载。"
    cqapi.send_group_msg(from_id, "".join(text))

def card(commandData, cqCodeList, message, from_id):
    try:
        cardname = "".join(commandData)
        i = cardnames.index(cardname)
        if cardtypes[i] == "單位" and cardsupertypes[i] == "英雄":
            cardcodei = cardcodes[i]
            res = [y for y in cardcodes if cardcodei in y]
            for j in res:
                title = "%s.png"%cardname
                imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(j[1],j)
                if cardtypes[cardcodes.index(j)] == "單位" and cardsupertypes[cardcodes.index(j)] == "英雄":
                    if len(j) > 7:
                        cqapi.send_group_msg(from_id, "%s的%s相关牌卡图：%s"%(cardname, j[7:9],image(title,imgurl)))
                    else:
                        cqapi.send_group_msg(from_id, "%s的卡图：%s"%(cardname,image(title,imgurl)))
        else:
            title = "%s.png"%cardname
            imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cardcodes[i][1],cardcodes[i][:7])
            cqapi.send_group_msg(from_id, "%s的卡图：%s"%(cardname,image(title,imgurl)))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。")
        
def cardart(commandData, cqCodeList, message, from_id):
    try:
        cardname = "".join(commandData)
        i = cardnames.index(cardname)
        if cardtypes[i] == "單位" and cardsupertypes[i] == "英雄":
            cardcodei = cardcodes[i]
            res = [y for y in cardcodes if cardcodei in y]
            for j in res:
                title = "%s.png"%cardname
                imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(j[1],j)
                if cardtypes[cardcodes.index(j)] == "單位" and cardsupertypes[cardcodes.index(j)] == "英雄":
                    if len(j) > 7:
                        cqapi.send_group_msg(from_id, "%s的%s相关牌原画：%s"%(cardname, j[7:9],image(title,imgurl)))
                    else:
                        cqapi.send_group_msg(from_id, "%s的原画：%s"%(cardname,image(title,imgurl)))
        else:
            title = "%s.png"%cardname
            imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(cardcodes[i][1],cardcodes[i][:7])
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(cardname,image(title,imgurl)))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。")
        
def cardcode(commandData, cqCodeList, message, from_id):
    try:
        cc = "".join(commandData)
        i = cardcodes.index(cc)
        cardname = cardnames[i]
        title1 = "%s.png"%cardname
        imgurl1 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cc[1],cc)
        imgurl2 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(cc[1],cc)
        cqapi.send_group_msg(from_id, "%s的卡图：%s"%(cardname,image(title,imgurl1)))
        cqapi.send_group_msg(from_id, "%s的原画：%s"%(cardname,image(title,imgurl2)))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌代码："+str(commandData)+"请检查是否输入错误。")
        

def deck(commandData, cqCodeList, message, from_id):
    champions.clear()
    followers.clear()
    spells.clear()
    global money
    print(str(commandData))
    try:
        deck = LoRDeck.from_deckcode(str(commandData))
        for i in list(deck):
            getinfo(str(i))
        for index in range(len(champions)):
            champions[index] = Converter('zh-hans').convert(champions[index])
        for index in range(len(followers)):
            followers[index] = Converter('zh-hans').convert(followers[index])
        for index in range(len(spells)):
            spells[index] = Converter('zh-hans').convert(spells[index])
        factions = []
        for card in deck.cards:
            factions.append(card.faction)
        factions = list(set(factions))
        for i in range(len(factions)):
            factions[i] = regions_name[regions_code.index(factions[i])]
        output = ""
        output += "卡组代码："+"".join(commandData)+"\r"
        output += "卡组地区："+",".join(factions)+"\r"
        output += "卡组费用："+str(money)
        output += "\r---------英雄---------\r"
        output += "\r".join(champions)
        output += "\r---------随从---------\r"
        output += "\r".join(followers)
        output += "\r---------法术---------\r"
        output += "\r".join(spells)
        print(output)
        cqapi.send_group_msg(from_id, "".join(output))
        
        money = 0
    except:
        cqapi.send_group_msg(from_id, "卡组代码解析失败")

bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        632727771,477949486
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ]
})

bot.command(deck, ["代码","卡组","code","deck"], {
    # deck 帮助
    "help": [
        "#deck - 卡组代码"
    ]
})

bot.command(错误170000, "错误170000", {
    # deck 帮助
    "help": [
        "#错误170000 - 170000怎么办"
    ]
})

bot.command(card, ["card","卡图"], {
    # deck 帮助
    "help": [
        "#卡图 - 展示卡图"
    ]
})

bot.command(cardart, ["art","原画"], {
    # deck 帮助
    "help": [
        "#原画 - 展示原画"
    ]
})

bot.command(cardcode, ["卡牌代码","cardcode","cc"], {
    # deck 帮助
    "help": [
        "#卡牌代码 - 展示代码对应的卡图和原画"
    ]
})

bot.start()

# 成功启动可以使用 指令 help, echo
# 使用 #echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助