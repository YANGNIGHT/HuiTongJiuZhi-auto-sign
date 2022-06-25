import requests
import zmail
import datetime
import json

qqmail = 'jinga36@163.com'  # 发件人邮箱账号
qqmailpwd = '123456'  # 发件人邮箱密码

# 读取账号密码
userdata = open("user.dat", "r", encoding="utf-8")
for x in userdata:
    if x and len(x.split()) == 3:
        user, pwd, email = x.split()

        username = user  # 账号
        password = pwd  # 密码

        #  获取id-token
        url = (
            f'https://token.jvtc.jx.cn/password/passwordLogin?username={username}&password={password}&appId=com.supwisdom.jvtc&deviceId=YrWODElvJR0DAN6bOOw8dTT9&osType=android'
        )
        response = requests.post(url)
        try:
            id_token = response.json()["data"]["idToken"]
            print("▁", end='')
        except:
            user_pwd = f'账号为:{username}\r\n密码为:{password}'
            print(f'\n有一个账号登录失败：\n{user_pwd}\n\n')
            print(response.json())
            continue

        # 1、获取ticket
        headers = {
            "x-id-token": id_token
        }
        url = "https://sso.jvtc.jx.cn/cas/login"
        params = {
            "service": "https://microserver4.jvtc.jx.cn/cas/loginapp?targetUrl=service%2Fsignin%2Fxqindex"
        }
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)

        tickets = response.headers['Location']  # 未经处理ticket
        ticket = tickets[tickets.index('ST'):]  # 传递给下一段处理后的ticket
        print("▂", end='')

        # 2、获取jsessionid
        params = (
            ('targetUrl', 'service/signin/xqindex'),
            ('ticket', ticket),
        )
        response = requests.get("https://microserver4.jvtc.jx.cn/cas/loginapp", params=params, allow_redirects=False)
        jsessionids = response.headers['Set-Cookie']
        jsessionid = jsessionids[jsessionids.index('JSESSIONID=') + 11:jsessionids.index('; path=/')]
        print("▃▄", end='')

        # 3、获取bladauth
        params = (
            ('targetUrl', 'service/signin/xqindex'),
        )
        cookies = {
            "JSESSIONID": jsessionid
        }

        response = requests.get("https://microserver4.jvtc.jx.cn/cas/loginapp", params=params, cookies=cookies,
                                allow_redirects=False)
        bladeauths = response.headers['Location']
        blade_auth = bladeauths[bladeauths.index('ey'):bladeauths.index('%26refreshtoken%3')]
        print("▅▆", end='')

        # 4、获取前一天位置信息等
        BladeAuth = {"Blade-Auth": "bearer " + blade_auth}
        yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)  # 前一天日期
        date = (('rq', yes_time.strftime('%Y-%m-%d')),)  # 格式化前一天输出日期
        response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin", params=date,
                                headers=BladeAuth)
        signdata = eval('{' + response.text[27:])  # 获取前一天位置信息等作为当天位置，更换位置需手动打卡一次
        name = signdata["data"]['xm']  # 这里是姓名
        xgh = signdata["data"]['xgh']  # 这里是学号
        try:
            yestoday_signtime = signdata["data"]['signin']['updateTime']  # 昨天打卡时间
            yesterday_address = signdata["data"]['signin']['address']  # 这里是adress地址
            yesterday_location = signdata["data"]['signin']['location']  # 位置
        except:
            yesterday_location = '江西省九江市濂溪区S22都九高速827号靠近九江职业技术学院濂溪校区 - 学生宿舍7栋'
            yesterday_address = yesterday_location

        # 判断今天是否打卡
        headers = {
            "Blade-Auth": "bearer " + blade_auth,
        }
        cookies = {"JSESSIONID": jsessionid}
        response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin",
                                headers=headers,
                                cookies=cookies)  # 打卡结果

        if len(response.text) > 550:  # 判断返回数据长度以判断是否打卡
            today_signdata = eval('{' + response.text[27:])  # 当天是否打卡
            today_location = today_signdata["data"]['signin']['location']  # 今天打卡位置
            toda_signtime = today_signdata["data"]['signin']['updateTime']  # 今天打卡时间
            print('▇█')
            print('有 %d 个数据存在>>>' % len(response.text), end='')
            print('年轻的' + name + '哟，今天已经打过卡啦！')
            print(toda_signtime + '在' + today_location + '成功打卡')
            print("▁▂▃▄▅▆▇█当前账户已完成█▇▆▅▄▃▂▁\n\n")
        else:
            # 打卡
            payload = {"jzqk": "3", "schsjcrq": "0", "hsbg": "null", "dqqdw": "0", "drzt": "0", "xyhs": "0",
                       "stzk": "0",
                       "stzkxq": "", "sfmj": "0", "sfzzxn": "0", "sfmjxq": "", "sfscgfxdq": "0", "sfscgfxdqxq": "",
                       "gfxljs": "0", "gfxljsxq": "", "wzsfbd": "0", "bdfs": "0", "cc": "", "ccpz": "null",
                       "dbrq": "",
                       "bdqswz": "", "bdjswz": "", "location": yesterday_location,
                       "address": yesterday_address, "xgh": xgh}  # 打卡提交的信息
            headers = {
                "Blade-Auth": "bearer " + blade_auth,
            }

            response = requests.post("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/submit",
                                     json=payload,
                                     headers=headers, params=params)  # 尝试打卡
            print('▇█')

            # 再次查询是否已打卡
            headers = {
                "Blade-Auth": "bearer " + blade_auth,
            }
            cookies = {"JSESSIONID": jsessionid}
            response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin",
                                    headers=headers,
                                    cookies=cookies)  # 打卡结果
            today_signdata = eval('{' + response.text[27:])  # 格式化返回信息
            today_location = today_signdata["data"]['signin']['location']  # 今天打卡位置
            toda_signtime = today_signdata["data"]['signin']['updateTime']  # 今天打卡时间
            back = '   年轻的' + name + '哟，打卡成功啦！' if "操作成功" in response.text else '打卡失败'
            messge = toda_signtime + '\r\n在' + today_location + '成功打卡\r\n'
            print(back + '\n' + messge)

            # 打卡ip属地
            url1 = 'https://worldtimeapi.org/api/timezone/Asia/Shanghai'
            res1 = requests.get(url1)
            data = json.loads(res1.text)
            ip = data["client_ip"]
            t = data["datetime"]
            t = t[:19]
            url3 = "https://whois.pconline.com.cn/ip.jsp?ip=" + ip
            res3 = requests.get(url3)
            ipdata = res3.text
            ttime = datetime.datetime.strptime(str(t), "%Y-%m-%dT%H:%M:%S")
            now_time = ('北京时间：' + str(ttime))
            location = ('当前服务器ip为:%s\r\n属地为:%s' % (ip, ipdata.strip()))
            print(location)
            
            # 邮箱通知
            mail_content = {
                'from': '慧通九职打卡',
                "subject": now_time + back,
                "Content_text": messge + location + '\r\n如有任何问题，请联系开发者：QQ：2983346017'  # 打卡情况
            }
            server = zmail.server(qqmail, qqmailpwd)  # 登录邮箱
            server.send_mail(email, mail_content)  # email为收件人 #发送邮件
