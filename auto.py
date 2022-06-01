import requests
import zmail
import datetime
import json

qqmail = 'jinga36@163.com'  # 发件人邮箱账号
qqmailpwd = '123456'  # 发件人邮箱密码

# 读取账号密码
fhandle = open("user.dat", "r", encoding="utf-8")
for x in fhandle:
    if x and len(x.split()) == 3:
        user, pwd, email = x.split()

        username = user  # 账号
        password = pwd  # 密码

        # 0、获取idtoken
        data = {
            "password": password,
            "username": username
        }

        url = (
            'https://token.jvtc.jx.cn/password/passwordLogin?'
        )
        phone = ('&appId=com.supwisdom.jvtc&geo=&deviceId=YmDAwpLUEAQDAOBg3MUu9xbE&osType=android')
        urls = url + 'username=' + username + '&' + 'password=' + password + phone

        response = requests.post(urls)

        var = response.text  # 未经处理的登录token
        if "Bad credentials" in var:
            print('账号或密码错误，请尝试重新登录：')
        else:
            idtoken = var[var.index('ey'):-27]  # 去除token多余参数
            print('''
=================================idtoken=================================
%s
=========================================================================
                '''
                  % idtoken
                  )

            # 1、获取第一个session
            params = (
                ('service', 'https://microserver4.jvtc.jx.cn/cas/loginapp?targetUrl=service%2Fsignin%2Fxqindex'),
            )

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://sso.jvtc.jx.cn",
                "Referer": "https://sso.jvtc.jx.cn/cas/login?service=https%3A%2F%2Fmicroserver4.jvtc.jx.cn%2Fcas%2Floginapp%3FtargetUrl%3Dservice%252Fsignin%252Fxqindex",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            response = requests.post("https://sso.jvtc.jx.cn/cas/login", params=params, data=data, headers=headers)

            session = response.headers['Set-Cookie']  # 未经处理session
            first_session = session[
                            session.index('SESSION=') + 8:session.index('; Path')]  # 登录后获取的处理后的第一个session
            print('''
=================================session=================================
%s
=========================================================================
            '''
                  % first_session
                  )  # 传递给第二段代码的session

            # 2、获取ticket
            params = (
                ('service', 'https://microserver4.jvtc.jx.cn/cas/loginapp?targetUrl=service%2Fsignin%2Fxqindex'),
            )

            data = {
                "_eventId": "submit",
                "currentMenu": "1",
                "execution": "e1s1",
                "failN": "-1",
                "password": password,
                "rememberMe": "true",
                "username": username
            }

            cookies = {
                "SESSION": first_session
            }

            response = requests.post("https://sso.jvtc.jx.cn/cas/login", params=params, data=data, headers=headers,
                                     cookies=cookies,
                                     allow_redirects=False)

            tickets = response.headers['Location']  # 未经处理ticket
            ticket = tickets[tickets.index('ST'):]
            print('''
=================================ticket==================================
%s
=========================================================================
                '''
                  % ticket
                  )  # 传递给下一段处理后的ticket

            # 3、获取jsessionid
            params = (
                ('targetUrl', 'service/signin/xqindex'),
                ('ticket', ticket),
            )

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection": "keep-alive",
                "Referer": "https://sso.jvtc.jx.cn/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            response = requests.get("https://microserver4.jvtc.jx.cn/cas/loginapp", params=params, headers=headers,
                                    allow_redirects=False)

            jsessionids = response.headers['Set-Cookie']
            jsessionid = jsessionids[
                         jsessionids.index('JSESSIONID=') + 11:jsessionids.index('; path=/')]
            print('''
===============================jsessionid================================
%s
=========================================================================
                '''
                  % jsessionid
                  )

            # 4、获取bladauth
            params = (
                ('targetUrl', 'service/signin/xqindex'),
            )

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            cookies = {
                "JSESSIONID": jsessionid
            }

            response = requests.get("https://microserver4.jvtc.jx.cn/cas/loginapp", params=params, headers=headers,
                                    cookies=cookies,
                                    allow_redirects=False)
            bladeauths = response.headers['Location']
            blade_auth = bladeauths[bladeauths.index('ey'):bladeauths.index('%26refreshtoken%3')]
            print('''
=================================bladauth=================================
%s
==========================================================================
                '''
                  % blade_auth
                  )

            # 获取前一天位置信息等
            BladeAuth = {"Blade-Auth": "bearer " + blade_auth}
            now_time = datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')
            yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)  # 前一天日期
            date = (('rq', yes_time.strftime('%Y-%m-%d')),)  # 格式化前一天输出日期
            response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin", params=date,
                                    headers=BladeAuth)
            signdata = eval('{' + response.text[27:])  # 获取前一天位置信息等作为当天位置，更换位置需手动打卡一次
            name = signdata["data"]['xm']  # 这里是姓名
            xgh = signdata["data"]['xgh']  # 这里是学号
            yestoday_signtime = signdata["data"]['signin']['updateTime']  # 昨天打卡时间
            yesterday_address = signdata["data"]['signin']['address']  # 这里是adress地址
            yesterday_location = signdata["data"]['signin']['location']  # 位置

            # 判断今天是否打卡
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Authorization": "Basic YXBwOmFwcF9zZWNyZXQ=",
                "Blade-Auth": "bearer " + blade_auth,
                "Connection": "keep-alive",
                "Content-Type": "application/json;charset=UTF-8",
                "Referer": "https://microserver4.jvtc.jx.cn/h5/pages/service/signin/xqindex",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            cookies = {"JSESSIONID": jsessionid}
            response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin", headers=headers,
                                    cookies=cookies)  # 打卡结果

            if len(response.text) > 550:  # 判断返回数据长度以判断是否打卡
                today_signdata = eval('{' + response.text[27:])  # 当天是否打卡
                today_location = today_signdata["data"]['signin']['location']  # 今天打卡位置
                toda_signtime = today_signdata["data"]['signin']['updateTime']  # 今天打卡时间
                print('''
=================================今天打卡结果=================================
%s\n
'有 %d 个数据存在>>>已打卡'
============================================================================
                                '''
                      % (response.text, len(response.text))
                      )

                back = '   年轻的' + name + '哟，今天已经打过卡啦！'
                messge = toda_signtime + '在' + today_location + '成功打卡       '
            else:
                # 打卡
                payload = {"jzqk": "3", "schsjcrq": "0", "hsbg": "null", "dqqdw": "0", "drzt": "0", "xyhs": "0",
                           "stzk": "0",
                           "stzkxq": "", "sfmj": "0", "sfzzxn": "0", "sfmjxq": "", "sfscgfxdq": "0", "sfscgfxdqxq": "",
                           "gfxljs": "0", "gfxljsxq": "", "wzsfbd": "0", "bdfs": "0", "cc": "", "ccpz": "null", "dbrq": "",
                           "bdqswz": "", "bdjswz": "", "location": yesterday_location,
                           "address": yesterday_address, "xgh": xgh}
                headers = {
                    "Host": "microserver4.jvtc.jx.cn",
                    "Connection": "keep-alive",
                    "Content-Length": "533",
                    "Sec-Fetch-Mode": "cors",
                    "Origin": "https://microserver4.jvtc.jx.cn",
                    "Blade-Auth": "bearer " + blade_auth,
                    "Authorization": "Basic YXBwOmFwcF9zZWNyZXQ=",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045738 Mobile Safari/537.36 SuperApp",
                    "X-Requested-With": "com.supwisdom.jvtc",
                    "Sec-Fetch-Site": "same-origin",
                    "Referer": "https://microserver4.jvtc.jx.cn/h5/pages/service/signin/xqindex",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cookie": "userToken=" + idtoken + "; Domain=microserver4.jvtc.jx.cn; Path=/; " + "JSESSIONID=" + jsessionid

                }

                response = requests.post("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/submit", json=payload,
                                         headers=headers, params=params)  # 尝试打卡

                print(response.text)

                # 再次查询是否已打卡
                headers = {
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Authorization": "Basic YXBwOmFwcF9zZWNyZXQ=",
                    "Blade-Auth": "bearer " + blade_auth,
                    "Connection": "keep-alive",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Referer": "https://microserver4.jvtc.jx.cn/h5/pages/service/signin/xqindex",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
                }

                cookies = {"JSESSIONID": jsessionid}
                response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin",
                                        headers=headers,
                                        cookies=cookies)  # 打卡结果
                today_signdata = eval('{' + response.text[27:])  # 格式化返回信息
                today_location = today_signdata["data"]['signin']['location']  # 今天打卡位置
                toda_signtime = today_signdata["data"]['signin']['updateTime']  # 今天打卡时间
                back = '   年轻的' + name + '哟，打卡成功啦！' if "操作成功" in response.text else '打卡失败'
                messge = toda_signtime + '在' + today_location + '成功打卡       '
                print(back)

            # 打卡ip属地
            url = "http://httpbin.org/ip"  # 也可以直接在浏览器访问这个地址
            r = requests.get(url)  # 获取返回的值
            ip = json.loads(r.text)["origin"]  # ip地址，取其中某个字段的值

            # 发送get请求
            url = f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query&lang=zh-CN'
            # 其中fields字段为定义接受返回参数，可不传；lang为设置语言，zh-CN为中文，可以传
            res = requests.get(url)  # 发送请求
            jsonobj = eval(res.text)  # 传回参数转为字典
            location = '当前服务器ip为:%s,属地为:%s' % (ip, jsonobj['country'] + jsonobj['regionName'] + jsonobj['city'])
            print(location)

            # 邮箱通知
            mail_content = {
                'from': '慧通九职打卡',
                "subject": now_time + back,
                "Content_text": messge + location  # 打卡情况
            }
            server = zmail.server(qqmail, qqmailpwd)  # 登录邮箱
            server.send_mail(email, mail_content)  # email为收件人 #发送邮件
