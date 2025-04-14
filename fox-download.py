# Code is taken from https://github.com/featurecat/go-dataset/issues/1
# and modified to work with python3

import requests
import json
import codecs
import time
import sys

def game_list(lastCode, username):
    values = {
    "type": 4,
    "lastCode": lastCode,
    "username": username,
    "RelationTag": 0}
    url = "http://happyapp.huanle.qq.com/cgi-bin/CommonMobileCGI/TXWQFetchChessList"
    response = requests.get(url, params=values)
    chesslist = json.loads(response.text)['chesslist']
    chessid = []
    fn = []
    for d in chesslist:
        chessid.append(d['chessid'])
        starttime = d['starttime'].split(' ')[0].replace('-', '.')
        id = d['chessid'][10:]
        blackenname = d['blackenname']
        whiteenname = d['whiteenname']
        fn.append(starttime + ' ' + blackenname + ' VS ' + whiteenname + ' (' + id + ')' + '.SGF')
    return chessid, fn

def download_sgf(cid, fn):
    values = { "chessid": cid }
    url = "http://happyapp.huanle.qq.com/cgi-bin/CommonMobileCGI/TXWQFetchChess"
    sgf = ""
    for i in range(10):
        try:
            response = requests.get(url, params=values)
            sgf = json.loads(response.text)['chess']
            break
        except Exception as e:
            if i == 9:
                print('ERROR')
                sys.exit(1)

    f = codecs.open('./games/' + fn, 'w', 'utf-8')
    f.write(sgf)
    f.close()

def download_all_user_sgf(username):
    chessid, fn = game_list("", username)
    idx = 0
    for i in range(len(chessid)):
        download_sgf(chessid[i], fn[i])
        print(i + 1, fn[i], 'LAST CODE:', lastCode)
        time.sleep(1)

    while True:
        lastCode = chessid[-1]
        idx += len(chessid)
        chessid, fn = game_list(lastCode, username)
        if len(chessid) == 0:
            break

        for i in range(len(chessid)):
            download_sgf(chessid[i], fn[i])
            print(i + idx + 1, fn[i], 'LAST CODE:', lastCode)
            time.sleep(1)

username = input('FOX user name: ')
download_all_user_sgf(username)
