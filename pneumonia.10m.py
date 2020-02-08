#!/Users/mablat/anaconda3/bin/python
# you can set your own python interperter

import requests as rq
import json
import os
from datetime import datetime

# you get set your own data url

data_url  = '/Users/mablat/bitbar-cache'

def get_result():
    url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
    c = rq.get(url)
    j = json.loads(c.content)
    s = j['data']['statistics']

    f = {}
    f['confirmed'] = s['confirmedCount']
    f['suspected'] = s['suspectedCount'] 
    f['died'] = s['deadCount']
    f['cured'] = s['curedCount']
    f['serious'] = s['seriousCount']
    return f


def prettify(s):
    confirmed = s['confirmed']
    suspected = s['suspected'] 
    died = s['died']
    cured = s['cured']
    serious = s['serious']
    return (str(suspected) + '/' + str(confirmed) + '/' + str(serious) + '/' + str(cured) + '/' + str(died) + ' | color = red')

def is_diff(before, after):
    if before['confirmed'] != after['confirmed']:
        backup(after)
        get_diff(before, after)
        return True
    else:
        return False

def get_diff(after, before):
    speak('new update on pneumonia')
    died = after['died'] - before['died']
    confirmed = after['confirmed'] - before['confirmed'] 
    suspected = after['suspected'] - before['suspected'] 
    cured = after['cured']- before['cured'] 
    serious = after['serious'] - before['serious']

    msg = ''
    if died > 0:
        msg = msg + str(died) + 'more dead,'
    
    if cured >0:
        msg = msg + str(cured) + 'more cured,'    

    if confirmed > 0:
        msg = msg + str(confirmed) + 'more confirmed'

    if suspected > 0:
        msg = msg + str(suspected) + 'more suspected,'
    
    speak(msg)

def speak(msg):
    voice  = 'Daniel '
    os.system('say -v ' + voice + msg) 

def backup(data):
    j = json.dumps(data)
    now = datetime.now()
    fname = now.strftime("%Y%m%d%H%M%s")
    f = open(data_url + '/' + fname + '.json', 'w')
    f.write(j)
    f.close()

def update_local(data):
    f = open(data_url + '/data.json', 'w')
    f.write(json.dumps(data))
    f.close()

def update():
    j1 = get_result();
    if not os.path.isfile(data_url + '/data.json'):
        update_local(j1)

    jf = open(data_url + '/data.json', 'r')
    j2 = json.loads(jf.read())

    if is_diff(j1, j2):
        print(prettify(j1))
        update_local(j1)
    else:
        print(prettify(j2))


update()