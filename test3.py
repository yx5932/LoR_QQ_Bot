#coding=utf-8
import os
import re
from calendar import c
from email.mime import image
from glob import glob1
from logging import exception
from pycqBot.cqApi import cqHttpApi, cqLog
from pycqBot.cqCode import at, image
from lor_deckcodes import LoRDeck, CardCodeAndCount
from pandas.core.frame import DataFrame
import csv
import json
import urllib
from unicodedata import name
from urllib.request import urlopen
import jsonpath
import pandas as pd
import random
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
landmarks = []
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
    text="如果账号地区没有问题（注册账号时如果没有开加速器，会导致账号归属地为中国（CHN），导致无法登陆游戏（错误代码1700000），检查账号所在地区攻略：账号地区检查），首次登陆游戏时也开了对应地区的加速器（首次登陆游戏时如果没有开账号对应地区的加速器，会被检测为账号归属地有误，从而导致黑号并无法登陆游戏），那就是网络问题网络问题网络问题，重要的事情说三遍。麻烦更换网络环境（开加速器的换节点，还是不行换个加速器；用有线网的改无线网；用无线网的换个别的无线网；WiFi不行就开流量；流量不行就换个运营商…）总而言之言而总之，更换网络环境。\r\r另外，自3.0版本以来，陆续有朋友在使用苹果设备的情况下，在试图更换账号时遇到170000问题，即使卸载游戏重装，也无法进入登陆界面。解决方法有如下2种：1、将设备格式化（恢复出厂设置），在格式化前请备份好自己的数据。 2、卸载LoR，然后更换其他地区的苹果账号再次下载。例如之前在美区苹果商店下载的LoR，可以切换成港区苹果账号再重新下载。"
    text2 = "[CQ:json,data={\"app\":\"com.tencent.miniapp_01\"&#44;\"appID\":\"100951776\"&#44;\"bthirdappforward\":true&#44;\"bthirdappforwardforbackendswitch\":true&#44;\"config\":{\"autoSize\":0&#44;\"ctime\":1647434637&#44;\"forward\":1&#44;\"height\":0&#44;\"token\":\"f2bbbe03c8b08dd0ca43c9f4b81ee7fb\"&#44;\"type\":\"normal\"&#44;\"width\":0}&#44;\"desc\":\"\"&#44;\"extra\":{\"app_type\":1&#44;\"appid\":100951776&#44;\"uin\":593261870}&#44;\"meta\":{\"detail_1\":{\"appType\":0&#44;\"appid\":\"1109937557\"&#44;\"desc\":\"【符文之地传说】遇到错误代码：170000怎么办？\"&#44;\"gamePoints\":\"\"&#44;\"gamePointsUrl\":\"\"&#44;\"host\":{\"nick\":\"Simple。\"&#44;\"uin\":593261870}&#44;\"icon\":\"https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1640166716\"&#44;\"preview\":\"https://pic.ugcimg.cn/7f74e4a7257f9f775e35b12b13048f71/jpg1\"&#44;\"qqdocurl\":\"https://b23.tv/44G2W45\"&#44;\"scene\":1036&#44;\"shareTemplateData\":{}&#44;\"shareTemplateId\":\"8C8E89B49BE609866298ADDFF2DBABA4\"&#44;\"showLittleTail\":\"\"&#44;\"title\":\"哔哩哔哩\"&#44;\"url\":\"m.q.qq.com/a/s/45b00d54e8887f6b76c394a526996193\"}}&#44;\"prompt\":\"&#91;QQ小程序&#93;哔哩哔哩\"&#44;\"ver\":\"0.0.0.1\"&#44;\"view\":\"view_8C8E89B49BE609866298ADDFF2DBABA4\"}]"
    cqapi.send_group_msg(from_id, text2)

def card(commandData, cqCodeList, message, from_id):
    commandData = check_chn(" ".join(commandData))
    try:
        # cardname = " ".join(commandData)
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
        print(output)
        cqapi.send_group_msg(from_id, "%s的卡图：%s"%(commandData, image(title,imgurl)+output))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。")

def GetFileList(FindPath): 
    FileList = [] 
    FileList_full = []
    FileNames=os.listdir(FindPath) 
    if (len(FileNames)>0): 
        for fn in FileNames: 
            fullfilename=os.path.join(FindPath,fn) 
            FileList_full.append(fn)
            FileList.append(fn.split(".")[0])
    return FileList,FileList_full
    
def cardart(commandData, cqCodeList, message, from_id):
    commandData = check_chn(" ".join(commandData))
    filenamelist,filelist_full = GetFileList("image")
    print(filenamelist)
    if "桃桃" in commandData and str(from_id) == "632727771":
        if commandData in filenamelist:
            print("[CQ:image,file=file:///image/%s,subType=0]"%filelist_full[filenamelist.index(commandData)])
            cqapi.send_group_msg(from_id, "%s："%commandData+"[CQ:image,file=file:///image/%s,subType=0]"%filelist_full[filenamelist.index(commandData)]+"\r-----loryx.wiki-----")
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
        
def cardcode(commandData, cqCodeList, message, from_id):
    commandData = check_chn(commandData)
    try:
        cc = "".join(commandData)
        i = cardcodes.index(cc)
        cardname = cardnames[i]
        title1 = "%s.png"%cardname
        imgurl1 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cc[1],cc)
        imgurl2 = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s-full.png"%(cc[1],cc)
        cqapi.send_group_msg(from_id, "%s的卡图：%s"%(cardname,image(title1,imgurl1))+"%s的原画：%s"%(cardname,image(title1,imgurl2)))
    except:
        cqapi.send_group_msg(from_id, "未检索到卡牌代码："+str(commandData)+"请检查是否输入错误。")
        
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
            landmarks[index] = Converter('zh-hans').convert(landmarks[index])
        print(champions,followers,spells,landmarks)
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
        print(output)
        cqapi.send_group_msg(from_id, "".join(output))
        
        money = 0
    except:
        cqapi.send_group_msg(from_id, "卡组代码解析失败")

def leaderboard(commandData, cqCodeList, message, from_id):
    input = "".join(commandData)
    shards = ['americas', 'americas', 'europe', 'europe','apac', 'apac']
    shards_input = ['na', '北美', 'eu', '欧洲','亚太', 'apac']
    playerid = []
    playerlp = []
    playerdc = []
    factions = []
    lbchampions = []
    if input in shards_input:
        lb_url = r"https://lormaster.herokuapp.com/leaderboard/"+shards[shards_input.index(input)]
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
                print(lbchampions)
            else:
                playerdc.extend("没有检索到卡组")
        output = "=======%s前5======="%input
        for i in range(5):
            rank = i+1
            output += "\rid:%s, 排名：%s\r"%(playerid[i],rank)
            if playerdc[i] != "没有检索到卡组":
                output += "-----卡组-----\r%s\r"%lbchampions[i]
                output += "---卡组代码---\r%s\r"%deckcode[i]
            else:
                output += "没有检索到卡组\r"
        cqapi.send_group_msg(from_id, "".join(output))
    else:
        cqapi.send_group_msg(from_id, "请检查输入的地区代号是否有误")

def sendimg(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "[CQ:image,file=file:///桃桃.jpg,subType=0]")

def video(commandData, cqCodeList, message, from_id):
    upid,indexs,title,bvid,link,date = [],[],[],[],[],[]
    loadlist = ["C:/wwwroot/submit.loryx.wiki/upload/KKX.csv","C:/wwwroot/submit.loryx.wiki/upload/听雨.csv", "C:/wwwroot/submit.loryx.wiki/upload/yx.csv"]
    month1 = ["年1月","年2月","年3月","年4月","年5月","年6月","年7月","年8月","年9月"]
    month2 = ["年01月","年02月","年03月","年04月","年05月","年06月","年07月","年08月","年09月"]
    day1 = ["月1日","月2日","月3日","月4日","月5日","月6日","月7日","月8日","月9日"]
    day2 = ["月01","月02","月03","月04","月05","月06","月07","月08","月09"]
    for i in loadlist:
        print(i)
        with open(i, encoding='UTF-8-sig') as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                if row[0]:
                    upid.append(row[0].strip())
                    indexs.append(row[1])
                    title.append(row[2])
                    bvid.append(row[3].strip())
                    link.append(row[4].replace("?spm_id_from=333.999.0.0","/").strip())
                    datee = row[5]
                    for i in range(9):
                        datee = datee.replace(month1[i],month2[i]).replace(day1[i],day2[i])
                    date.append(datee.replace("年","-").replace("月","-").replace("日","").strip())
            videodata = DataFrame({"upid" : upid, "indexs" : indexs, "title" : title, "bvid" : bvid, "link" : link, "date" : date})
            videodata = videodata.sort_values(by='date', ascending=False)
    if commandData[0]:
        # print(videodata[videodata.upid==commandData[0]])
        if commandData[0] == "yx" or commandData[0] == "YX":
            commandData[0] = "yx5932"
        elif commandData[0] == "卡卡西" or commandData[0] == "kkx":
            commandData[0] = "KKX"
        elif commandData[0] == "秦时" or commandData[0] == "秦时听雨" or commandData[0] == "秦時聽雨":
            commandData[0] = "听雨"
        if commandData[0] in upid:
            # pos = [i for i in range(len(lst)) if value==lst[i]]
            newvd = videodata[videodata.upid==commandData[0]]
            newvd = newvd.drop_duplicates(subset=['bvid']).sort_values(by='date', ascending=False)
            print(newvd)
            upvideosinfo = newvd.values.tolist()
            print(upvideosinfo,len(upvideosinfo))
            output2 = ""
            count = 0
            for i in range(5):
                try:
                    output2 += "%s、%s\r视频链接：%s\r"%(i+1,upvideosinfo[i][2],upvideosinfo[i][4])
                    count += 1
                except:
                    output1 = "Up主 %s 最近的%s条视频：\r"%(commandData[0],count)
                    cqapi.send_group_msg(from_id, output1+output2)
                    return
            output1 = "Up主 %s 最近的%s条视频：\r"%(commandData[0],count)
            cqapi.send_group_msg(from_id, output1+output2)
            return
        elif videodata[videodata.indexs.str.contains(commandData[0])].empty == False:
            newvd = videodata[videodata.indexs.str.contains(commandData[0])]
            newvd = newvd.drop_duplicates(subset=['bvid']).sort_values(by='date', ascending=False)
            print(newvd)
            upvideosinfo = newvd.values.tolist()
            print(upvideosinfo,len(upvideosinfo))
            output2 = ""
            count = 0
            for i in range(3):
                try:
                    output2 += "%s、%s\r视频链接：%s\r"%(i+1,upvideosinfo[i][2],upvideosinfo[i][4])
                    count += 1
                except:
                    output1 = "关于 %s 最近的%s条视频：\r"%(commandData[0],count)
                    cqapi.send_group_msg(from_id, output1+output2)
                    return
            output1 = "关于 %s 最近的%s条视频：\r"%(commandData[0],count)
            cqapi.send_group_msg(from_id, output1+output2)
            return
        else:
            output = "没有找到关于%s的视频"%commandData[0]
            cqapi.send_group_msg(from_id, output)
            return

def music(commandData, cqCodeList, message, from_id):
    filelist,filelist_full = GetFileList("music")
    print(filelist_full)
    idx = random.randint(0,len(filelist_full))
    print(idx, filelist_full[idx])
    cqcode = "[CQ:record,file=file:///music/%s]"%filelist_full[idx]
    print(cqcode)
    cqapi.send_group_msg(from_id, cqcode)
    
def voice(commandData, cqCodeList, message, from_id):
    cqcode = "[CQ:tts,text=这是一条测试消息]"
    cqapi.send_group_msg(from_id, cqcode)

def randomplayer(commandData, cqCodeList, message, from_id):
    selectedplayer = random.randint(0,1)
    cqapi.send_group_msg(from_id, "%s获得了先手禁用权。"%commandData[selectedplayer])
    
bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        632727771
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo + 文本 - 复读机"
    ]
})

bot.command(deck, ["代码","卡组","code","deck"], {
    # deck 帮助
    "help": [
        "#deck/#code/#代码/#卡组 + 卡组代码 ： 解析卡组代码"
    ]
})

bot.command(错误170000, "错误170000", {
    # deck 帮助
    "help": [
        "#错误170000 ： 170000怎么办"
    ]
})

bot.command(card, ["card","卡图"], {
    # deck 帮助
    "help": [
        "#卡图/#card ： 展示卡图"
    ]
})

bot.command(cardart, ["art","原画"], {
    # deck 帮助
    "help": [
        "#原画/#art + 卡牌代码 ： 展示原画"
    ]
})

bot.command(cardcode, ["卡牌代码","cardcode","cc"], {
    # deck 帮助
    "help": [
        "#卡牌代码/#cc + 卡牌代码 ： 展示代码对应的卡图和原画"
    ]
})

bot.command(leaderboard, ["排行榜","leaderboard","lb"], {
    # deck 帮助
    "help": [
        "#排行榜/#leaderboard/#lb + 地区（na/北美/eu/欧洲/apaca/亚太）- 展示对应地区前5玩家和卡组"
    ]
})

bot.command(sendimg, ["sendimg"], {
    # deck 帮助
    "help": [
        "#排行榜/#leaderboard/#lb + 地区（na/北美/eu/欧洲/apaca/亚太）- 展示对应地区前5玩家和卡组"
    ]
})

bot.command(video, ["视频","video"], {
    # deck 帮助
    "help": [
        "【#视频/#video + 卡组名】 ： 指定卡组的教学视频\r"
        "【#视频/#video + up主id】 ： 该up主最近3条视频"
    ]
})

bot.command(music, ["音乐","music"], {
    # deck 帮助
    "help": [
        "【#音乐/#music】 ： 随机播放一首LoR的bgm"
    ]
})

bot.command(voice, ["share","分享"], {
    # deck 帮助
    "help": [
        "【#音乐/#music】 ： 随机播放一首LoR的bgm"
    ]
})

bot.command(randomplayer, ["随机","random","rd"], {
    # deck 帮助
    "help": [
        "【#random + 玩家1 + 玩家2】 ： 随机选择一个玩家"
    ]
})

bot.start()

# 成功启动可以使用 指令 help, echo
# 使用 #echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助