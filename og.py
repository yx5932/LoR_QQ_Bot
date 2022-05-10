#coding=utf-8
from email.mime import image
from glob import glob
from logging import exception
from pycqBot.cqApi import cqHttpApi, cqLog
from pycqBot.cqCode import at, image
from lor_deckcodes import LoRDeck, CardCodeAndCount
import csv
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
landmarks = []
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

def check_chn(commandData):
    with open('简繁对照.csv', encoding='UTF-8-sig') as f:
        simpC, tradC = [],[]
        f_csv = csv.reader(f)
        for row in f_csv:
            simpC.append(row[0])
            tradC.append(row[1])
        if "".join(commandData) in simpC:
            commandData = tradC[simpC.index("".join(commandData))]
            return commandData
    return commandData
    
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
    elif cardtypes[index] == "地標":
        cost = cardcosts[index]
        info += '%s'%costs[cost]
        info += cardnames[index] + ' ' + cardnum + '张'
        landmarks.append(info)
        

# 启用日志 默认日志等级 DEBUG
cqLog()

cqapi = cqHttpApi()

# echo 函数
def echo(commandData, cqCodeList, message, from_id):
    # 发送群消息
    cqapi.send_group_msg(from_id, " ".join(commandData))

def 错误170000(commandData, cqCodeList, message, from_id):
    # 发送群消息
    text="如果账号地区没有问题（注册账号时如果没有开加速器，会导致账号归属地为中国（CHN），导致无法登陆游戏（错误代码1700000），检查账号所在地区：account.riotgames.com），首次登陆游戏时也开了对应地区的加速器（首次登陆游戏时如果没有开账号对应地区的加速器，会被检测为账号归属地有误，从而导致黑号并无法登陆游戏），那就是网络问题网络问题网络问题，重要的事情说三遍。麻烦更换网络环境（开加速器的换节点，还是不行换个加速器；用有线网的改无线网；用无线网的换个别的无线网；WiFi不行就开流量；流量不行就换个运营商…）总而言之言而总之，更换网络环境。\r\r另外，自3.0版本以来，陆续有朋友在使用苹果设备的情况下，在试图更换账号时遇到170000问题，即使卸载游戏重装，也无法进入登陆界面。解决方法有如下2种：1、将设备格式化（恢复出厂设置），在格式化前请备份好自己的数据。 2、卸载LoR，然后更换其他地区的苹果账号再次下载。例如之前在美区苹果商店下载的LoR，可以切换成港区苹果账号再重新下载。"
    cqapi.send_group_msg(from_id, "".join(text))

def card(commandData, cqCodeList, message, from_id):
    commandData = check_chn(" ".join(commandData))
    try:
        i = cardnames.index(commandData)
        cardcodei = cardcodes[i]
        if cardnames[cardcodes.index(cardcodei)] == cardnames[cardcodes.index(cardcodei[:7])]:
            cardcodei = cardcodei[:7]
        title = "%s.png"%commandData
        imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cardcodei[1],cardcodei)
        res = [y for y in cardcodes if cardcodei[:7] in y]
        output = "你可能还想找此牌的相关卡牌：\r"
        for j in res:
            output += "%s：%s\r"%(j,cardnames[cardcodes.index(j)])
        output += "你可以使用#cc %s来查看对应卡牌代码的卡图和原画"%res[0]
        if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, "%s的卡图：%s"%(commandData, image(title,imgurl)+output+"\r-----loryx.wiki-----"))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。卡查功能正在准备繁简对照表，欢迎补充：https://docs.qq.com/sheet/DVFlGT0VXd3BVUVJi")
        
def cardart(commandData, cqCodeList, message, from_id):
    commandData = check_chn(" ".join(commandData))
    if str(from_id) == "545327542":
        if commandData == "桃桃":
            title = "桃桃"
            imgurl = "https://i.bmp.ovh/imgs/2022/03/67459d5bfd4acaa6.jpg"
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+"\r-----loryx.wiki-----"))
            return
        elif commandData == "旗袍桃桃":
            title = "旗袍桃桃"
            imgurl = "https://i.bmp.ovh/imgs/2022/03/1d3a13d0e7a46348.jpg"
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+"\r-----loryx.wiki-----"))
            return
        elif commandData == "沉默桃桃":
            title = "沉默桃桃"
            imgurl = "https://i.bmp.ovh/imgs/2022/03/227f970f5fc5b41d.jpg"
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+"\r-----loryx.wiki-----"))
            return
        elif commandData == "桃桃牵kkx":
            title = "桃桃牵kkx"
            imgurl = "https://i.bmp.ovh/imgs/2022/03/084818ccef3db149.jpg"
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+"\r-----loryx.wiki-----"))
            return
        elif commandData == "桃桃牵老师":
            title = "桃桃牵老师"
            imgurl = "https://i.bmp.ovh/imgs/2022/03/5200cc3a7730d3b4.jpg"
            cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+"\r-----loryx.wiki-----"))
            return
    try:
        i = cardnames.index(commandData)
        cardcodei = cardcodes[i]
        title = "%s.png"%commandData
        imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(cardcodei[1],cardcodei)
        res = [y for y in cardcodes if cardcodei[:7] in y]
        output = "你可能还想找此牌的相关卡牌：\r"
        for j in res:
            output += "%s：%s\r"%(j,cardnames[cardcodes.index(j)])
        output += "你可以使用#cc %s来查看对应卡牌代码的卡图和原画"%res[0]
        if str(from_id) != "477949486":
            output += "-------loryx.wiki-------"
        cqapi.send_group_msg(from_id, "%s的原画：%s"%(commandData, image(title,imgurl)+output+"\r"))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。卡查功能正在准备繁简对照表，欢迎补充：https://docs.qq.com/sheet/DVFlGT0VXd3BVUVJi")
        
def getregion(deck):
    factions = []
    for card in deck.cards:
            factions.append(card.faction)
    factions = list(set(factions))
    for i in range(len(factions)):
        factions[i] = regions_name[regions_code.index(factions[i])]
    return factions

def getchampions(deck):
    champ = []
    for i in list(deck):
        cardcode = i[2:]
        if cardsupertypes[cardcodes.index(cardcode)] == "英雄":
            champ.append(str(cardnames[cardcodes.index(cardcode)]))
    return "，".join(champ)
    
def deck(commandData, cqCodeList, message, from_id):
    commandData = check_chn(commandData)
    champions.clear()
    followers.clear()
    spells.clear()
    landmarks.clear()
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
        for index in range(len(landmarks)):
            spells[index] = Converter('zh-hans').convert(landmarks[index])
        factions = getregion(deck)
        output = ""
        output += "卡组代码："+"".join(commandData)+"\r"
        output += "卡组地区："+",".join(factions)+"\r"
        output += "卡组费用："+str(money)
        if champions:
            output += "\r---------英雄---------\r"
            output += "\r".join(champions)
        output += "\r---------随从---------\r"
        output += "\r".join(followers)
        output += "\r---------法术---------\r"
        output += "\r".join(spells)
        if landmarks:
            output += "\r---------地标---------\r"
            output += "\r".join(landmarks)
        if str(from_id) != "477949486":
            output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, "".join(output))
        money = 0
    except:
        cqapi.send_group_msg(from_id, "卡组代码解析失败")

def cardcode(commandData, cqCodeList, message, from_id):
    try:
        cc = "".join(commandData)
        i = cardcodes.index(cc)
        cardname = cardnames[i]
        title1 = "%s.png"%cardname
        imgurl1 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cc[1],cc)
        imgurl2 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(cc[1],cc)
        output = "%s的卡图：%s"%(cardname,image(title1,imgurl1))+"%s的原画：%s"%(cardname,image(title1,imgurl2)+"\r")
        if str(from_id) != "477949486":
            output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, output)
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌代码："+str(commandData)+"请检查是否输入错误。")

def leaderboard(commandData, cqCodeList, message, from_id):
    lbinput = str(commandData[0])
    if len(commandData) > 1:
        commandData[1] = " ".join(commandData[1:])
    shards = ['americas', 'americas', 'americas', 'europe', 'europe','europe','apac', 'apac','apac']
    shards_input = ['na', '北美', '美服','eu', '欧洲','欧服','亚太', 'apac','亚服']
    playerid = []
    playerlp = []
    playerdc = []
    factions = []
    lbchampions = []
    if lbinput in shards_input:
        lb_url = r"https://lormaster.herokuapp.com/leaderboard/"+shards[shards_input.index(lbinput)]
        print(lb_url)
        lb_html = urllib.request.urlopen(lb_url)
        lb_html_json = json.load(lb_html)
        playerid.extend(jsonpath.jsonpath(lb_html_json,"$..name"))
        playerlp.extend(jsonpath.jsonpath(lb_html_json,"$..lp"))
        deckcode = jsonpath.jsonpath(lb_html_json,"$..deck_code")
        champions.clear()
        for i in deckcode:
            if i:
                playerdc.extend(i)
                deck = LoRDeck.from_deckcode(i)
                factions.extend("".join(getregion(deck)))
                lbchampions.append(getchampions(deck))
            else:
                lbchampions.append("")
                playerdc.extend("没有检索到卡组")
        if len(commandData) > 1:
            try:
                rank = int(commandData[1]) - 1
                output = "=======%s第%s名======="%(lbinput,commandData[1])
                output += "\r玩家昵称：%s\r"%playerid[rank]
                output += "玩家胜点：%s\r"%playerlp[rank]
                if playerdc[rank] != "没有检索到卡组":
                    output += "玩家近期卡组：%s\r"%lbchampions[rank]
                    output += "卡组代码：%s\r"%deckcode[rank]
                else:
                    output += "玩家卡组：没有检索到卡组\r"
            except:
                playername = str(commandData[1])
                if playername in playerid:
                    rank = playerid.index(playername)
                    output = "=======%s第%s名======="%(lbinput,str(rank+1))
                    output += "\r玩家昵称：%s\r"%playerid[rank]
                    output += "玩家胜点：%s\r"%playerlp[rank]
                    if playerdc[rank] != "没有检索到卡组":
                        output += "玩家近期卡组：%s\r"%lbchampions[rank]
                        output += "卡组代码：%s\r"%deckcode[rank]
                    else:
                        output += "玩家卡组：没有检索到卡组\r"
                else:
                    output = "没有检索到玩家：%s，可能是因为该玩家还不是大师。\r"%playername
            if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
        else:
            output = "=======%s前10======="%lbinput
            for i in range(10):
                rank = i+1
                output += "\rid:%s, 排名：%s\r"%(playerid[i],rank)
                if playerdc[i] != "没有检索到卡组":
                    output += "-----卡组-----\r%s\r"%lbchampions[i]
                    output += "---卡组代码---\r%s\r"%deckcode[i]
                else:
                    output += "没有检索到卡组\r"
            if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, "".join(output))
    else:
        cqapi.send_group_msg(from_id, "请检查输入的地区代号是否有误")
        
bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        1060536929,545327542,818251816,750653891,1085146271
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "【#echo + 文本】 ： 复读机"
    ]
})

bot.command(deck, ["代码","卡组","code","deck"], {
    # deck 帮助
    "help": [
        "【#deck/#code/#代码/#卡组 + 卡组代】 ： 解析卡组代码"
    ]
})

bot.command(错误170000, "错误170000", {
    # deck 帮助
    "help": [
        "【#错误170000】 ： 170000怎么办"
    ]
})

bot.command(card, ["card","卡图"], {
    # deck 帮助
    "help": [
        "【#卡图/#card】 ： 展示卡图"
    ]
})

bot.command(cardart, ["art","原画"], {
    # deck 帮助
    "help": [
        "【#原画/#art + 卡牌代码】 ： 展示原画"
    ]
})

bot.command(cardcode, ["卡牌代码","cardcode","cc"], {
    # deck 帮助
    "help": [
        "【#卡牌代码/#cc + 卡牌代码】 ： 展示代码对应的卡图和原画"
    ]
})

bot.command(leaderboard, ["排行榜","leaderboard","lb"], {
    # deck 帮助
    "help": [
        "【#排行榜/#leaderboard/#lb + 地区（na/北美/美服/eu/欧洲/欧服/apaca/亚太/亚服）】- 展示对应地区前5玩家和卡组"
        "【#排行榜 + 地区 + 排名或玩家id】 ： 展示对应地区指定排名或id的大师玩家的信息"
    ]
})


bot.start()


# 成功启动可以使用 指令 help, echo
# 使用 #echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助