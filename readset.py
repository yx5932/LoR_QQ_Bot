import json
import urllib
from unicodedata import name
from urllib.request import urlopen
import jsonpath
import pandas as pd
from langconv import *

seturls = [r"https://dd.b.pvp.net/latest/set1/zh_tw/data/set1-zh_tw.json",r"https://dd.b.pvp.net/latest/set2/zh_tw/data/set2-zh_tw.json",r"https://dd.b.pvp.net/latest/set3/zh_tw/data/set3-zh_tw.json",r"https://dd.b.pvp.net/latest/set4/zh_tw/data/set4-zh_tw.json",r"https://dd.b.pvp.net/latest/set5/zh_tw/data/set5-zh_tw.json"]
cardcodes = []
cardnames = []
for i in seturls:
    setinfo_html = urllib.request.urlopen(i)
    setinfo_html_json = json.load(setinfo_html)
    # champion_abilities = ["%s"%str(champion_name)]
    # print(setinfo_html_json[0])
    codes = jsonpath.jsonpath(setinfo_html_json,'$..cardCode')
    names = jsonpath.jsonpath(setinfo_html_json,'$..name')
    cardcodes.extend(codes)
    cardnames.extend(names)

for index in range(len(cardnames)):
    cardnames[index] = Converter('zh-hans').convert(cardnames[index])

    # champion_abilities.append(''.join(jsonpath.jsonpath(C_Ability_html_json,'$.data.%s.passive.name'%champion_id)))
# for i in jsonpath.jsonpath(C_Ability_html_json,'$.data.%s.spells[*].name'%champion_id):
#     champion_abilities.append(i)
#     # print(champion_abilities)