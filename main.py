#coding=utf-8
import os
from email.mime import image
import re
from glob import glob
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
import random
import pandas as pd
from pandas.tseries.offsets import Day
from langconv import *
import time

cardcosts = []
cardcodes = []
cardcodes_en = []
cardnames = []
cardnames_tw = []
cardnames_en = []
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

with open("files/sets.json",'r',encoding='utf-8') as load_f:
    sets_json = json.load(load_f)
    cardcosts.extend(jsonpath.jsonpath(sets_json,'$..cost'))
    cardcodes.extend(jsonpath.jsonpath(sets_json,'$..cardCode'))
    cardnames_tw.extend(jsonpath.jsonpath(sets_json,'$..name'))
    cardregions.extend(jsonpath.jsonpath(sets_json,'$..regions'))
    cardtypes.extend(jsonpath.jsonpath(sets_json,'$..type'))
    cardsupertypes.extend(jsonpath.jsonpath(sets_json,'$..supertype'))
    cardrarities.extend(jsonpath.jsonpath(sets_json,'$..rarity'))
    # cardengnames.extend(jsonpath.jsonpath(sets_json,'$..rarity'))

with open("files/sets_en.json",'r',encoding='utf-8') as load_f:
    sets_json2 = json.load(load_f)
    cardnames_en.extend(jsonpath.jsonpath(sets_json2,'$..name'))
    cardnames_en = [x.lower() for x in cardnames_en]
    cardcodes_en.extend(jsonpath.jsonpath(sets_json2,'$..cardCode'))


for i in range(len(cardnames_tw)):
    cardnames.append(Converter('zh-hans').convert(cardnames_tw[i]))


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
    text="[CQ:json,data={\"app\":\"com.tencent.miniapp_01\"&#44;\"appID\":\"100951776\"&#44;\"bthirdappforward\":true&#44;\"bthirdappforwardforbackendswitch\":true&#44;\"config\":{\"autoSize\":0&#44;\"ctime\":1647434637&#44;\"forward\":1&#44;\"height\":0&#44;\"token\":\"f2bbbe03c8b08dd0ca43c9f4b81ee7fb\"&#44;\"type\":\"normal\"&#44;\"width\":0}&#44;\"desc\":\"\"&#44;\"extra\":{\"app_type\":1&#44;\"appid\":100951776&#44;\"uin\":593261870}&#44;\"meta\":{\"detail_1\":{\"appType\":0&#44;\"appid\":\"1109937557\"&#44;\"desc\":\"【符文之地传说】遇到错误代码：170000怎么办？\"&#44;\"gamePoints\":\"\"&#44;\"gamePointsUrl\":\"\"&#44;\"host\":{\"nick\":\"Simple。\"&#44;\"uin\":593261870}&#44;\"icon\":\"https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1640166716\"&#44;\"preview\":\"https://pic.ugcimg.cn/7f74e4a7257f9f775e35b12b13048f71/jpg1\"&#44;\"qqdocurl\":\"https://b23.tv/44G2W45\"&#44;\"scene\":1036&#44;\"shareTemplateData\":{}&#44;\"shareTemplateId\":\"8C8E89B49BE609866298ADDFF2DBABA4\"&#44;\"showLittleTail\":\"\"&#44;\"title\":\"哔哩哔哩\"&#44;\"url\":\"m.q.qq.com/a/s/45b00d54e8887f6b76c394a526996193\"}}&#44;\"prompt\":\"&#91;QQ小程序&#93;哔哩哔哩\"&#44;\"ver\":\"0.0.0.1\"&#44;\"view\":\"view_8C8E89B49BE609866298ADDFF2DBABA4\"}]"
    cqapi.send_group_msg(from_id, "".join(text))

def card(commandData, cqCodeList, message, from_id):
    commandData = check_chn(" ".join(commandData))
    print(len(commandData))
    if len(commandData) == 0:
        cqapi.send_reply(message, "你还没有输入想要查询的卡牌")
        return
    print(commandData, commandData in cardnames)
    try:
        if commandData in cardnames:
            i = cardnames.index(commandData)
        elif commandData in cardnames_tw:
            i = cardnames_tw.index(commandData)
        else:
            i = cardcodes.index(cardcodes_en[cardnames_en.index(commandData.lower())])
        cardcodei = cardcodes[i]
        if cardnames[cardcodes.index(cardcodei)] == cardnames[cardcodes.index(cardcodei[:7])]:
            cardcodei = cardcodei[:7]
        title = "%s.png"%commandData
        imgurl = "http://dd.b.pvp.net/latest/set%s/zh_tw/img/cards/%s.png"%(cardcodei[1],cardcodei)
        res = [y for y in cardcodes if cardcodei[:7] in y]
        output = "你可能还想找此牌的相关卡牌：\r"
        for j in res:
            output += "%s ：%s\r"%(j,cardnames[cardcodes.index(j)])
        output += "你可以使用#cc %s来查看对应卡牌代码的卡图和原画"%res[0]
        if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
        cqapi.send_reply(message, "%s的卡图：%s"%(commandData, image(title,imgurl)+output+"\r"))
    except:
        clist = []
        output = "您正在查询的卡牌是否为："
        en_input = False
        for i in range(len(cardnames)):
            if commandData in cardnames[i]:
                clist.append(i)
        if len(clist) == 0:
            for i in range(len(cardnames_tw)):
                if commandData in cardnames_tw[i]:
                    clist.append(i)
        if len(clist) == 0:
            for i in range(len(cardnames_en)):
                if commandData.lower() in cardnames_en[i]:
                    clist.append(i)
                en_input = True
        print(clist)
        print(len(clist))
        if len(clist) != 0 and en_input == False:
            for cnumber in range(len(clist)):
                if cnumber < 10:
                    output += "%s、%s（代码：%s） "%(cnumber+1,cardnames[clist[cnumber]],cardcodes[clist[cnumber]])
            output += "\r您可以使用 #卡图 + 卡牌名称 来查看对应卡图，或使用 #cc + 卡牌代码 来查看对应卡牌的卡图和原画\r"
            if str(from_id) != "477949486":
                output += "-------loryx.wiki-------"
            cqapi.send_reply(message, output)
        elif len(clist) != 0 and en_input:
            for cnumber in range(len(clist)):
                if cnumber < 10:
                    output += "%s、%s（代码：%s）  "%(cnumber+1,cardnames_en[clist[cnumber]],cardcodes_en[clist[cnumber]])
            output += "\r您可以使用 #卡图 + 卡牌名称 来查看对应卡图，或使用 #cc + 卡牌代码 来查看对应卡牌的卡图和原画\r"
            if str(from_id) != "477949486":
                output += "-------loryx.wiki-------"
            cqapi.send_reply(message, output)
        else:
            cqapi.send_reply(message, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。卡查功能正在准备繁简对照表，欢迎补充：https://docs.qq.com/sheet/DVFlGT0VXd3BVUVJi")
        
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
    if str(from_id) == "545327542":
        if commandData in filenamelist:
            print("[CQ:image,file=file:///image/%s,subType=0]"%filelist_full[filenamelist.index(commandData)])
            cqapi.send_reply(message, "%s："%commandData+"[CQ:image,file=file:///image/%s,subType=0]"%filelist_full[filenamelist.index(commandData)]+"\r-----loryx.wiki-----")
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
        cqapi.send_reply(message, "%s的原画：%s"%(commandData, image(title,imgurl)+output+"\r"))
    except:
        cqapi.send_reply(message, "未检索到卡牌："+str(commandData)+"请检查是否输入错误。卡查功能正在准备繁简对照表，欢迎补充：https://docs.qq.com/sheet/DVFlGT0VXd3BVUVJi")
        
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
    
def decode(commandData, cqCodeList, message, from_id):
    champions.clear()
    followers.clear()
    spells.clear()
    landmarks.clear()
    global money
    print(str(commandData))
    try:
        deck = LoRDeck.from_deckcode(str(commandData).strip())
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
            output += "\r-----loryx.wiki-----"
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
        cqapi.send_reply(message, output)
    except:
        cqapi.send_reply(message, "未检索到卡牌代码："+str(commandData)+"请检查是否输入错误。")

def changename(i):
    with open('files/中中.csv', encoding='UTF-8-sig') as f:
        simpC, nicknameC = [],[]
        f_csv = csv.reader(f)
        for row in f_csv:
            simpC.append(row[0])
            nicknameC.append(row[1])
        if i in nicknameC:
            i = simpC[nicknameC.index(i)]
            return i
    return i

def deck(commandData, cqCodeList, message, from_id):
    print(commandData[0] == "all" or commandData[0] == "所有" or commandData[0] == "全")
    if commandData[0] == "all" or commandData[0] == "所有" or commandData[0] == "全":
        cqapi.send_group_msg(from_id, "所有卡组："+"[CQ:image,file=file:///image/卡组.png,subType=0]")
        return
    names = "、".join(commandData)
    tmp_lst = []
    test = r"files/csv天梯数据.csv"
    update_time = os.path.getmtime(test)
    timeoutput = '数据更新时间:{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(update_time)))
    print(timeoutput)
    with open('files/csv天梯数据.csv', encoding='UTF-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    deck_df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0]) 
    new_deck_df = deck_df
    for i in commandData:
        champname = changename(i)
        new_deck_df = new_deck_df[new_deck_df.deck.str.contains(champname)]
    if new_deck_df.empty == False:
        deckinfo = new_deck_df.values.tolist()
        count = 0
        output2 = ""
        for i in range(3):
            try:
                output2 += "%s、%s\r使用率：%s，胜率：%s\r平均交互：%s次，卡组类型：%s\r卡组代码：%s\r"%(count+1,deckinfo[i][0],deckinfo[i][1],deckinfo[i][2],deckinfo[i][4],deckinfo[i][5],deckinfo[i][6])
                count += 1
            except:
                output1 = "关于“%s”的卡组如下：\r%s\r"%(names,timeoutput)
                output = output1 + output2 + "\r交互：当出牌主动权发生更替时，算作1次交互，例如己方打出1个单位后轮到敌方操作，则交互次数+1。\r卡组类型：\r[CQ:image,file=file:///image/卡组类型说明.png,subType=0]\r"
                if str(from_id) != "477949486":
                    output += "-----loryx.wiki-----"
                cqapi.send_group_msg(from_id, output)
                return
        output1 = "关于“%s”的卡组如下：\r%s\r"%(names,timeoutput)
        output = output1 + output2 + "\r交互：当出牌主动权发生更替时，算作1次交互，例如己方打出1个单位后轮到敌方操作，则交互次数+1。\r卡组类型：\r[CQ:image,file=file:///image/卡组类型说明.png,subType=0]\r"
        if str(from_id) != "477949486":
            output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, output)
        return
    else:
        output = "没有找到关于“%s”的卡组，可能是如下原因中的一种：\r1、数据库中收录了版本中%s个常见卡组，你输入的英雄或许不在这些卡组中，完整的数据库卡组和代码列表可以使用指令：“#卡组 all” 或前往 https://loryx.wiki/guide/decksearch 查看。\r2、你输入的英雄名有误。输入格式可以参考：“#卡组 吉格斯” / “#卡组 小法 赛娜” / “#卡组 飞升” 等等，注意空格。\r3、你可能想解析卡组代码，请使用新的指令 “ #解码 / #解析 / #代码 / #decode / #code + 卡组代码”来解析卡组代码。"%(names,deck_df.iloc[:,0].size)
        if str(from_id) != "477949486":
            output += "-----loryx.wiki-----"
        cqapi.send_group_msg(from_id, output)
        return

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
        print("lencomD:",len(commandData))
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
            if commandData[1] == "yx5932":
                output = "=======%s第0名======="%(lbinput)
                output += "\r玩家昵称：yx5932"
                output += "\r玩家胜点：5932"
                cqapi.send_group_msg(from_id, "".join(output))
                return
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

def yx(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "yx的含义，就是yx")
    
def exppool(commandData, cqCodeList, message, from_id):
    output = "LoR的经验池："+"[CQ:image,file=file:///image/经验池.png,subType=0]\r"
    if str(from_id) != "477949486":
        output += "-----loryx.wiki-----"
    cqapi.send_group_msg(from_id, output)

def video(commandData, cqCodeList, message, from_id):
    upid,indexs,title,bvid,link,date,date2 = [],[],[],[],[],[],[]
    source = []
    uplist = ["KKX","听雨","yx","CCY"]
    for i in uplist:
        source.append("C:/wwwroot/submit.loryx.wiki/upload/%s.xlsx"%i)
    month1 = ["年1月","年2月","年3月","年4月","年5月","年6月","年7月","年8月","年9月"]
    month2 = ["年01月","年02月","年03月","年04月","年05月","年06月","年07月","年08月","年09月"]
    day1 = ["月1日","月2日","月3日","月4日","月5日","月6日","月7日","月8日","月9日"]
    day2 = ["月01","月02","月03","月04","月05","月06","月07","月08","月09"]
    for i in source:
        videodata = pd.read_excel(i,sheet_name=0)
        videodata.columns = ["upid","indexs","title","bvid","link","date"]
        date2.append(videodata['date'].tolist())
        basetime = pd.to_datetime("1899/12/30")
        videodata.date = videodata.date.apply(lambda x: basetime+Day(x))
        videodata.date = videodata.date.apply(lambda x: f"{x.year}年{x.month}月{x.day}日")
        # videodata = videodata.sort_values(by='date', ascending=False)
        upid.append(videodata['upid'].tolist())
        indexs.append(videodata['indexs'].tolist())
        title.append(videodata['title'].tolist())
        bvid.append(videodata['bvid'].tolist())
        link.append(videodata['link'].tolist())
        date.append(videodata['date'].tolist())
    upid = sum(upid,[])
    indexs = sum(indexs,[])
    title = sum(title,[])
    bvid = sum(bvid,[])
    link = sum(link,[])
    date = sum(date,[])
    date2 = sum(date2,[])
    videodata = pd.DataFrame({'upid':upid, 'indexs':indexs, 'title':title, 'bvid':bvid, 'link':link, 'date':date, 'date2':date2})
    print(videodata)
    if commandData[0]:
        # print(videodata[videodata.upid==commandData[0]])
        inputid = ["yx","YX","卡卡西","kkx","秦时","秦时听雨","秦時聽雨","嘻嘻歪","ccy","dwbbbbbb","DWB"]
        listedid = ["yx5932","yx5932","KKX","KKX","听雨","听雨","听雨","CCY","CCY","dwb","dwb"]
        if commandData[0] in inputid:
            print(commandData[0])
            commandData[0] = listedid[inputid.index(commandData[0])]
            print(commandData[0])
        if commandData[0] in listedid:
            # pos = [i for i in range(len(lst)) if value==lst[i]]
            newvd = videodata[videodata["upid"]==commandData[0]]
            newvd = newvd.drop_duplicates(subset=['bvid']).sort_values(by='date2', ascending=False)
            upvideosinfo = newvd.values.tolist()
            output2 = ""
            count = 0
            if len(commandData) > 1:
                if commandData[1] == "new":
                    output2 += "%s、%s\r上传日期：%s，视频/文章链接：%s\r"%(count+1,upvideosinfo[0][2],upvideosinfo[0][5],upvideosinfo[0][4])
                    count += 1
            else:
                for i in range(5):
                    try:
                        output2 += "%s、%s\r上传日期：%s，视频/文章链接：%s\r"%(i+1,upvideosinfo[i][2],upvideosinfo[i][5],upvideosinfo[i][4])
                        count += 1
                    except:
                        output1 = "Up主 %s 最近的%s条视频：\r"%(commandData[0],count)
                        output = output1 + output2
                        if str(from_id) != "477949486":
                            output += "-----loryx.wiki-----"
                        cqapi.send_group_msg(from_id, output)
                        return
            output1 = "Up主 %s 最近的%s条视频/文章：\r"%(commandData[0],count)
            output = output1 + output2
            if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
            cqapi.send_group_msg(from_id, output)
            return
        elif videodata[videodata.indexs.str.contains(commandData[0])].empty == False:
            newvd = videodata[videodata.indexs.str.contains(commandData[0])]
            newvd = newvd.drop_duplicates(subset=['bvid']).sort_values(by='date2', ascending=False)
            print(newvd)
            upvideosinfo = newvd.values.tolist()
            print(upvideosinfo,len(upvideosinfo))
            output2 = ""
            count = 0
            for i in range(3):
                try:
                    output2 += "%s、%s\rup主：%s，关键词：%s\r视频/文章链接：%s\r"%(i+1,upvideosinfo[i][2],upvideosinfo[i][0],upvideosinfo[i][1],upvideosinfo[i][4])
                    count += 1
                except:
                    output1 = "关于 %s 最近的%s条视频/文章：\r"%(commandData[0],count)
                    output = output1 + output2
                    if str(from_id) != "477949486":
                        output += "-----loryx.wiki-----"
                    cqapi.send_group_msg(from_id, output)
                    return
            output1 = "关于 %s 最近的%s条视频/文章：\r"%(commandData[0],count)
            output = output1 + output2
            if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
            cqapi.send_group_msg(from_id, output)
            return
        else:
            output = "没有找到关于%s的视频/文章\r"%commandData[0]
            if str(from_id) != "477949486":
                output += "-----loryx.wiki-----"
            cqapi.send_group_msg(from_id, output)
            return
        
def music(commandData, cqCodeList, message, from_id):
    filelist,filelist_full = GetFileList("music")
    idx = random.randint(0,len(filelist_full))
    cqapi.send_group_msg(from_id, "收到请求啦，马上发送一首LoR中的随机BGM")
    cqcode = "[CQ:record,file=file:///music/%s]"%filelist_full[idx]
    print(cqcode)
    cqapi.send_group_msg(from_id, cqcode)
        
def lux(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "[CQ:image,file=file:///gifs/lux.gif,subType=1]")
    
def roadmap(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "[CQ:image,file=file:///image/2022规划.jpg]")

def deckperformance(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "卡组对战胜率：\r"+"[CQ:image,file=file:///image/卡组对阵数据.png]")
    
def rankreward(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "排位奖励：\r"+"[CQ:image,file=file:///image/排位奖励.png]")

def pcdownload(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "PC客户端可以通过以下链接下载（全服同客户端）：\r"+"https://bacon.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.live.sea.exe")

def usefullinks(commandData, cqCodeList, message, from_id):
    cqapi.send_group_msg(from_id, "LoR中文百科（含大量LoR相关资料）：https://loryx.wiki/ \r注册下载安装：https://loryx.wiki/guide/howtoplay\r170000怎么办？：https://www.bilibili.com/video/BV1Nq4y1i7gb/\rM站：卡组查询、游戏资讯等：https://lor.mobalytics.gg/decks\rLMT：国人制作的网站，战绩查询和卡组很方便，还有很好用的记牌器：https://app.lormaster.com/\r战绩查询2：https://dak.gg/lor\r卡组名称自定义：https://deckname.loryx.wiki/\rAR站：卡组排行榜数据更新较快：https://runeterra.ar/\r数据查询网站，纯英文https://www.llorr-stats.com/")

def surr(commandData, cqCodeList, message, from_id):
    surrlist_path = "files/htlist.txt"
    file1=open(surrlist_path,'r')
    content1=file1.readlines()
    print(content1)
    cqapi.send_group_msg(from_id, "【互投指令使用说明】\r1、请使用“#互投登记 你的信息”进行登记，进入互投等待区，例如：“#互投登记 欧服 迷你海兽#1234 QQ:1258012580”，登记时最好带上qq号，以防别人找你互投时联系不上你。\r2、请在互投结束后使用指令“#取消登记 你的信息”将自己移出互投等待区，等待下次有互投需求时再次登记。\r3、请勿擅自将他人信息移出等待区。")
    if len(content1) == 0:
        cqapi.send_group_msg(from_id, "暂时没有人在等待互投")
    else:
        cqapi.send_group_msg(from_id, "以下玩家正在等待互投\r===============\r"+"".join(content1))
    file1.close()

def surr_check(commandData, cqCodeList, message, from_id):
    surrlist_path = "files/htlist.txt"
    surr_player_info = " ".join(commandData)
    file1=open(surrlist_path,'r+')
    content1 = file1.readlines()
    f1length = len(content1)
    print(f1length)
    if f1length >12:
        cqapi.send_group_msg(from_id, "当前已有很多人正在等待互投，你可以使用 #互投 寻找他们进行互投")
        return
    file1.write("%s\r"%surr_player_info)
    cqapi.send_group_msg(from_id, "添加成功：%s"%surr_player_info)
    file1.close()
    
def surr_uncheck(commandData, cqCodeList, message, from_id):
    surrlist_path = "files/htlist.txt"
    surr_player_info = " ".join(commandData)
    file1=open(surrlist_path,'r')
    content1=file1.readlines()
    file1.close()
    poped = False
    notclean = True
    surrlist_length = len(content1)
    i = 0
    while notclean:
        if surr_player_info in content1[i]:
            content1.remove(content1[i])
            poped = True
            surrlist_length -= 1
            if i == surrlist_length:
                notclean = False
        else:
            i += 1
            if i == surrlist_length:
                notclean = False
    file2=open(surrlist_path,'w+')
    file2.write("".join(content1))
    if poped == False:
        cqapi.send_group_msg(from_id, "互投列表中未检索到该玩家")
    else:
        cqapi.send_group_msg(from_id, "已成功移除：%s"%surr_player_info)
    file2.close()

def randomplayer(commandData, cqCodeList, message, from_id):
    if from_id == 904531989:
        selectedplayer = random.randint(0,1)
        cqapi.send_group_msg(from_id, "%s获得了先手禁用权。"%commandData[selectedplayer])
    else:
        cqapi.send_group_msg(from_id, "此功能为比赛群专用。")
    
bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有

    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "【#echo + 文本】 ： 复读机"
    ]
})

bot.command(decode, ["解码","解析","代码","decode","code"], {
    # deck 帮助
    "help": [
        "【#解析/#代码/#decode/#code + 卡组代码】 ： 解析卡组代码"
    ]
})

bot.command(错误170000, ["错误170000","170000","17000"], {
    # deck 帮助
    "help": [
        "【#错误170000/#170000】 ： 170000怎么办"
    ]
})

bot.command(card, ["card","卡图"], {
    # deck 帮助
    "type": "all",
    "help": [
        "【#卡图/#card】 ： 展示卡图"
    ]
})

bot.command(cardart, ["art","原画"], {
    # deck 帮助
    "type": "all",
    "help": [
        "【#原画/#art + 卡牌代码】 ： 展示原画"
    ]
})

bot.command(cardcode, ["卡牌代码","cardcode","cc"], {
    # deck 帮助
    "type": "all",
    "help": [
        "【#卡牌代码/#cc + 卡牌代码】 ： 展示代码对应的卡图和原画"
    ]
})

bot.command(leaderboard, ["排行榜","leaderboard","lb"], {
    # deck 帮助
    "help": [
        "【#排行榜/#leaderboard/#lb + 地区（na/北美/美服/eu/欧洲/欧服/apaca/亚太/亚服）】- 展示对应地区前5玩家和卡组\r【#排行榜 + 地区 + 排名或玩家id】 ： 展示对应地区指定排名或id的大师玩家的信息"
    ]
})

bot.command(exppool, ["经验池","exp"], {
    # deck 帮助
    "help": [
        "【#经验池/#exp】- LoR的经验池"
    ]
})

bot.command(video, ["视频","video","sp"], {
    # deck 帮助
    "help": [
        "【#视频/#video + 卡组名】 ： 指定卡组的教学视频\r【#视频/#video + up主id】 ： 该up主最近3条视频"
    ]
})

bot.command(music, ["音乐","music"], {
    # deck 帮助
    "help": [
        "【#音乐/#music】 ： 随机播放一首LoR的bgm"
    ]
})

bot.command(lux, ["lux","拉克丝","Lux"], {
    # deck 帮助
    "help": [
        "【#lux/#拉克丝】 ： 拉克丝给你点了个赞"
    ]
})

bot.command(deck, ["卡组","卡组查询","deck"], {
    # deck 帮助
    "help": [
        "【#卡组/#卡组查询/#deck + 英雄名】 ： 查询含有某英雄的卡组名（多个英雄用一个空格分隔）\r【#卡组/#卡组查询/#deck + all/所有/全】 ： 查看数据库中的所有卡组"
    ]
})

bot.command(roadmap, ["线路图","roadmap","规划图"], {
    # deck 帮助
    "help": [
        "【#线路图】 ： LoR 2022年上半年线路规划"
    ]
})

bot.command(randomplayer, ["随机","random","rd"], {
    # deck 帮助
    "help": [
        "【#random + 玩家1 + 玩家2】 ： 随机选择一个玩家"
    ]
})

bot.command(deckperformance, ["卡组表现"], {
    # deck 帮助
    "help": [
        "【#卡组表现】 ： 展示卡组对局胜率表"
    ]
})

bot.command(rankreward, ["排位奖励"], {
    # deck 帮助
    "help": [
        "【#排位奖励】 ： 展示排位奖励"
    ]
})

bot.command(pcdownload, ["PC","pc"], {
    # deck 帮助
    "help": [
        "【#pc】 ： PC客户端下载链接"
    ]
})

bot.command(usefullinks, ["网址","网站","实用链接"], {
    # deck 帮助
    "help": [
        "【#网址/网站/实用链接】 ： PC客户端下载链接"
    ]
})

bot.command(surr, ["互投"], {
    # deck 帮助
    "help": [
        "【#互投】 ： 展示正在等待互投的玩家清单\r【#互投登记】：登记互投玩家信息（服务器 id#tag）\r【#取消登记】：取消登记互投玩家信息（服务器 id#tag）"
    ]
})

bot.command(surr_check, ["互投登记"], {
})

bot.command(surr_uncheck, ["取消登记"], {
})

bot.command(yx, ["yx","YX"], {
    # deck 帮助
    "help": [
        "【#yx】- yx是什么意思"
    ]
})


bot.start()


# 成功启动可以使用 指令 help, echo
# 使用 #echo Hello World
# bot 会回复消息 "Hello World"
# 并且 help 帮助添加 echo 帮助