#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
cron: 1 0,18 * * *
new Env('锦鲤-红叶Python版');
改自jd_jinli_hongbao.ts文件
'''


import os,json,random,time,re,string,functools,asyncio,sys
try:
    import requests
except Exception as e:
    print(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


## 助力前n个账号
jinliCount = 1
## 锦鲤log (json格式)
jinliLogs = [
    {"random":"25076811","log":"1650125108738~1azSH56m6nqMDF0ZWNEUTAyMQ==.RVNWdGBGUFJ0ZkZXVTpmDBY5czYRVyp9L0VJVWhnWFQddi9FGx0=.8d461930~6,1~5ACB2080984BA00B286EA5C9E6B50E9CBA870DAB~1klo6jn~C~ThdBXBQIbWkZF0FfWxAMbxdRABxyahp5DRkEBgYeVxhBFxkTUgUbcG0ZeAkaAw58GVQZRRQeFFAEGHFoGn8PGAR3YR1DHkIWaBkXVkRcFA4EGRdCRRAMFgQDAAEHAAMFBQIFBgUGAwcDFxkTQVdSFg8XQUVCRkJSQFMXHRRFU1UXDxdXUEZCQEFAVBMaEEZQWxcPagIeAAMAGQwdBwIaBRkAaB0UWFwWDwQZE1VBFA4XA1dTU1QBDVYBBwBTA1UFAAUACAFWVAVXBgMEVwBXBQEXGRNYQhQOF1xlUFIQGhZBFw8AAAcGBQcABAEOBQUMGRdfWhQIFFAAAQJUV1NTUA1XDFAPBgUMV1cNAwIEBAYDBFNXV1ADBgUHA1JUUAAWGRdTQVQQDBYXGRdfQBAMFnRFRV1TEnVbWEVARVNAGhR8W1YfFB4UWlRDFwsUAwAMBQAHExoQRVdHFw9qBwIEABkCAwlrHhRGWhcPahRbZlVRBAQdBxAaFlx6ZhMaEAcAGwEbABQeFAUFGwAfBhAaFgQDDQEDABQYF1EABQFXV1VQUQ1TD1MPAAYNV1MOAAICBwcDAFBUV1YABwUDAFFUVgMXGRNXEGsYF1xaUBQIFFJTU1NXUEZCFhkXVFsUCBRBFxkXUl8QDBZCBhsDGAYUGBdWU25AEAwWBQcXHRRQUhYPF0dQWFZZWQgHAAEBBA4FBBcZE1tYFA5uBBkBGgJrGBdXWV5REAwWBAMAAQcAAwUFAwwJAUwHeFhTQ1JmYG5Dc3hxd29jB2IEVGFwTnx3CQgbVGlgVWRiXURRXGR0bnNZB1dwRWt9B0VefWVdQHAGc3JzSANEegVZcVF5f0BnTFFFZWVCdXF2bwRlS0EGeHBnWHp1XV11ZnRtegN3BXtgDVFsY1lzfE4MQ3JlDmBycAV6eltva1dlWkF6cnMLfGVCfXFGRUhwdmRbVHBRB3dyAWZ4ZVFqbl5sXnpGY11XbEFGcndzfHhOAUJ2cndbe2FWeVd5bwZmTVpcd2JjW3dNBWR8S11WfkNnRn9GRQt0Q3RGfVZ/fHxmdFpzYlpYcnV4ZHdLUUh0Tlpye3BjCnlORgZ3c3MKfEMNdnFLVVBsQwxnZVgORGZedwRxSFV2fXZgUnR1DllwZ0VZdFtzAnROeG1/A3daf05zZ3JJe1x0Z3dAVlxnV3FlAAJ4W3dfd3ZCTXNLc18YVgdWDVJTUAFKQhkET0hMdEphd1FmbmBVeXNzYHlxY2NscmBsc3NjQWViTWBncGQHcnNCRmdwSl1jZGdkfHBzf3txQnxpZXd0ZWByBHRwY3tidHRkaX5gYHxzQgFpcHBZYW1gYGdySlJhYVJ4dndVf2JzZ2NjcEUOYHNgUgxIAwZfBF8MSxQeFFlGUhcLFBBL~1v8h2wk"},
]


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')

# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/ql/config/config.sh')
            except:
                a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/jd/config/config.sh')
            except:
                a=eval(env)
        else:
            a=eval(env)
    except:
        a=''
    return a

# v4
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 


# 随机ua
def ua():
    sys.path.append(os.path.abspath('.'))
    try:
        from jdEnv import USER_AGENTS as a
    except:
        a='jdapp;iPad;10.5.0;;;M/5.0;appBuild/168052;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22ZNU0D2VrYWVuEQS5YJu0CzrsYtqyDNYyCtYnZwZrYtUyCNS2Y2TsDq%3D%3D%22%2C%22sv%22%3A%22CJGkDM4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1650125106%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPad; CPU OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;'
    return a

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

## 获取cooie
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量JD_COOKIE\n')    
        return cookie_list

    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except:
                    pass
        return a
cookie_list=Judge_env().main_run()



# 正式代码部分

def postApi(fn, body, cookie):
    headers = {
        'Cookie': cookie,
        # 'User-Agent': 'jdapp;iPad;10.5.0;;;M/5.0;appBuild/168052;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22ZNU0D2VrYWVuEQS5YJu0CzrsYtqyDNYyCtYnZwZrYtUyCNS2Y2TsDq%3D%3D%22%2C%22sv%22%3A%22CJGkDM4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1650125106%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPad; CPU OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
        'User-Agent': ua(),
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://happy.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://happy.m.jd.com/babelDiy/zjyw/3ugedFa7yA6NhxLN5gw2L3PF9sQC/index.html?asid=448106744',
        'Accept-Language': 'zh-cn',
    }
    params = (
        ('appid', 'jinlihongbao'),
        ('functionId', fn),
        ('loginType', '2'),
        ('client', 'jinlihongbao'),
        ('t', gettimestamp()),
        ('clientVersion', '10.5.0'),
        ('osVersion', '-1'),
    )
    data = {
        'body': json.dumps(body)
    }
    print({
        'headers': headers,
        'params': params,
        'data': data
    })
    response = requests.post('https://api.m.jd.com/api', headers=headers, params=params, data=data, timeout=10)
    return response

def api(fn, body, cookie):
    for n in range(3):
        res = postApi(fn, body, cookie).json()
        # print(res)
        if res['rtn_code'] != 403:
            return res
    return ''

def randomItem(a):
    length = len(a)
    if length < 1:
        return ''
    return a[random.randint(0, length-1)]

def randomSleep():
    time.sleep(random.randint(10, 20))


def getPackets():
    # 打开红包
    for e,cookie in enumerate(cookie_list,start=1):
        if e > jinliCount:
            break
        print(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        try:
            packetCount = 1
            res = api('h5activityIndex', { "isjdapp": 1 }, cookie)
            for t in res['data']['result']['redpacketConfigFillRewardInfo']:
                if t['packetStatus'] == 2:
                    packetAmount = t['packetAmount']
                    print(f'红包{packetCount}已拆过，获得{packetAmount}')
                elif t['packetStatus'] == 1:
                    print(f'红包{packetCount}可拆')
                    lg = randomItem(jinliLogs)
                    body = {
                        'random': lg['random'],
                        'log': lg['log'],
                        'sceneid': 'JLHBhPageh5'
                    }
                    res = api('h5receiveRedpacketAll', body, cookie)
                    print(res['data']['biz_msg'] + res['data']['result']['discount'])
                else:
                    print(packetCount + t['hasAssistNum'] + '/' + t['requireAssistNum'])
                packetCount += 1
        except:
            print('数据异常')
            continue
        randomSleep()
    randomSleep()

def getHelp(redPackets):
    fullCode = set()
    # 内部助力
    print('开始内部助力\n')
    for e,cookie in enumerate(cookie_list,start=1):
        print(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        try:
            for code in redPackets:
                if code in fullCode:
                    break
                lg = randomItem(jinliLogs)
                body = {
                    'redPacketId': code,
                    'followShop': 0,
                    'random': lg['random'],
                    'log': lg['log'],
                    'sceneid': 'JLHBhPageh5'
                }
                res = api('jinli_h5assist', body, cookie)
                resStatus = res['data']['result']['status']
                if resStatus == 0:
                    discount = res['data']['result']['assistReward']['discount']
                    print(f'助力成功：{discount}')
                elif resStatus == 3:
                    print('今日助力次数已满')
                elif res['data']['result']['statusDesc'] == '啊偶，TA的助力已满，开启自己的红包活动吧~':
                    fullCode.add(code)
        except:
            print('数据异常')
            continue
        randomSleep()
    randomSleep()

def getRedPackets(redPackets):
    # 获取红包id
    print('开始获取红包\n')
    for e,cookie in enumerate(cookie_list,start=1):
        if e > jinliCount :
            break
        try:
            print(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
            res = api('h5activityIndex', { "isjdapp": 1 }, cookie)
            redPacket = res['data']['result']['redpacketInfo']['id']
            print(f'红包id: {redPacket}\n')
            redPackets.add(redPacket)
        except:
            print('数据异常')
            continue
        randomSleep()
    randomSleep()

def main():
    print('锦鲤任务开始！\n')
    print(f'====================共{len(cookie_list)}个京东账号Cookie=========\n')


    redPackets = set()

    getRedPackets(redPackets)
    getHelp(redPackets)
    getPackets()



if __name__ == '__main__':
    main()
