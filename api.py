import json

import requests
import re
import random

#'下面这个函数用来判断信息开头的几个字是否为关键词'
#'如果是关键词则触发对应功能，群号默认为空'
#def keyword(message,uid):
#    requests.get(url='http://127.0.0.1:5711/send_group_msg?group_id={0}&message={1}团分{2}'.format(uid, message))
#    return message

def keyword(message, uid, gid = None):
    print('ggg')
    if message[0:3] == '300': # 300查团分, 格式为300+游戏名称，如 “300yaq”
        print('hhh')
        return zhanji(uid, gid, message[3:len(message)])
        
def zhanji(uid, gid, name):

#	'本功能参考300英雄官方api文档写成'
#	'有不理解的地方可以看看https://300report.jumpw.com/static/doc/openapi.txt'
    
#    url = 'https://300report.jumpw.com/api/getrole?name=' + name
#    menu = requests.get(url)
#    for i in menu.json()['Rank']:
#        if i['RankName'] == '团队实力排行':
#            tuanfen = i['Value']
    print('abc')
    if gid != None: # 如果是群聊信息
        print('bcd')
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:image,' r'text=' + str(name) + r']'))
    else: # 如果是私聊信息
        requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}团分{2}'.format(uid, name, tuanfen))