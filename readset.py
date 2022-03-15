from cmath import cos
import json
import urllib
from unicodedata import name
from urllib.request import urlopen
import jsonpath
import pandas as pd
from langconv import *
import emoji
from lor_deckcodes import LoRDeck, CardCodeAndCount

# seturls = ["sets.json","set2-zh_tw.json","set3-zh_tw.json","set4-zh_tw.json","set5-zh_tw.json"]
cardcosts = []
cardcodes = []
cardnames = []
cardregions = []
cardtypes = []
cardsupertypes = []
costs = ['⓪','①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮','⑯','⑰','⑱','⑲','⑳']
sets_json = ''
# for i in range(len(seturls)):

with open("sets.json",'r',encoding='utf-8') as load_f:
    sets_json = json.load(load_f)
    cardcosts.extend(jsonpath.jsonpath(sets_json,'$..cost'))
    cardcodes.extend(jsonpath.jsonpath(sets_json,'$..cardCode'))
    cardnames.extend(jsonpath.jsonpath(sets_json,'$..name'))
    cardregions.extend(jsonpath.jsonpath(sets_json,'$..regions'))
    cardtypes.extend(jsonpath.jsonpath(sets_json,'$..type'))
    cardsupertypes.extend(jsonpath.jsonpath(sets_json,'$..supertype'))
    print(sets_json)

champions = []
followers = []
spells = []
def getinfo(cardinfo):
    cardcode = cardinfo[2:]
    cardnum = cardinfo[:1]
    # setinfo_html = urllib.request.urlopen(i)
    print(cardcode)
    index = cardcodes.index(cardcode)
    info = ''
    print(cardsupertypes[index])
    if cardsupertypes[index] == "英雄":
        cost = cardcosts[index]
        info += emoji.emojize('%s'%costs[cost])
        info += cardnames[index] + ' ' + cardnum + '张'
        champions.append(info)
    elif cardtypes[index] == "單位":
        cost = cardcosts[index]
        info += emoji.emojize('%s'%costs[cost])
        info += cardnames[index] + ' ' + cardnum + '张'
        followers.append(info)
    elif cardtypes[index] == "法術":
        cost = cardcosts[index]
        info += emoji.emojize('%s'%costs[cost])
        info += cardnames[index] + ' ' + cardnum + '张'
        spells.append(info)
    # carddetail = jsonpath.jsonpath(sets_json,'$..[?(@.cardCode == %s)]'%cardcode)
    # print(carddetail)
    # champion_abilities = ["%s"%str(champion_name)]
    # print(setinfo_html_json[0])
    # codes = jsonpath.jsonpath(sets_json,'$..cardCode')
    # names = jsonpath.jsonpath(sets_json,'$..name')
    # cardcodes.extend(codes)
    # cardnames.extend(names)

    # for index in range(len(cardnames)):
    #     cardnames[index] = Converter('zh-hans').convert(cardnames[index])

    # champion_abilities.append(''.join(jsonpath.jsonpath(C_Ability_html_json,'$.data.%s.passive.name'%champion_id)))
# for i in jsonpath.jsonpath(C_Ability_html_json,'$.data.%s.spells[*].name'%champion_id):
#     champion_abilities.append(i)
#     # print(champion_abilities)

deck = LoRDeck.from_deckcode('CEBAIAIFB4WDANQIAEAQGDAUDAQSIJZUAIAQCBIFAEAQCBAA')
for i in deck.cards:
    getinfo(str(i))
print(emoji.emojize(champions[0]))
print(followers)
print(spells)
    