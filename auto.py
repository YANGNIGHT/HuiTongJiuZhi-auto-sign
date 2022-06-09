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

        # 1、获取idtoken
        data = {
            "password": password,
            "username": username
        }

        url = (
            'https://token.jvtc.jx.cn/password/passwordLogin?'
        )
        phone = '&appId=com.supwisdom.jvtc&geo=&deviceId=YmDAwpLUEAQDAOBg3MUu9xbE&osType=android'
        urls = url + 'username=' + username + '&' + 'password=' + password + phone

        response = requests.post(urls)

        var = response.text  # 未经处理的登录token
        if "Bad credentials" in var:
            print('账号或密码错误，请尝试重新登录：')
            # 邮箱通知
            mail_content = {
                'from': '慧通九职打卡',
                "subject": '账号或密码错误，请确认密码后重新提交',
                "Content_text": response.text  # 打卡情况
            }
            server = zmail.server(qqmail, qqmailpwd)  # 登录邮箱
            server.send_mail(email, mail_content)  # email为收件人 #发送邮件
        else:
            idtoken = var[var.index('ey'):-27]  # 去除token多余参数
            print("▁▂", end='')

            # 2、获取ticket
            params = (
                ('service', 'https://microserver4.jvtc.jx.cn/cas/loginapp?targetUrl=service%2Fsignin%2Fxqindex'),
            )

            data = {
                "_eventId": "submit",
                "captcha": "",
                "currentMenu": "1",
                "execution": "50a7daab-d773-4329-a770-541af86c8649_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuYlJ2R01JUmxySDhhSWU1VFZsYURCeGlMa3Y2Z2t1by9CSkwzY0U0OUtjb1Z2VkRTY0U2ZThZWkhGT0VEZDB4SGJIdlRFdGhFT0xMRFZQV2ErbzBVdE9XYUkxdHpPQjRYRlFXQzRwa1plYUh3VTh5a3FNSkxkSnZOSnNxK05xVExueDFpMVpPMk0vcjBJU0MzU0pWTmFJaEt2dm42SWpKZGFrVWdPN2hCT1VDbjFOMjlkdFRQNm12TGJFcnk2dkxhalBzYVFkNVN2ZktabGpBdnR1UGFRd2xXaVBHVlkvaUhFTy84ZVFQd1Ztbm44VSt6NlNFREVzVUdCSGN1TjZLS3pPMjBrcXdkQVUybENQQkN6SXN4akJ0YWQ2ZmhDUmMzdlNVYnlBa3MweGJLM3VjUDFkaHRMVnRWSzBHaXMxemZKYlhHRzVYYVhvZmdWNCtjYnkvODMvUmJTRGhidDdzcU54MTJKVWRmUllZL2ErbEdnc1I5d2l4K1E4QmJxakp3NFVjaE84d2J4U2FjYndkNUp3U2dDeTVseVpVcVdHRk40ZmJzOWZ6cTgySTdEZVRtMkYxTUhzVFhCRzBEQlNvNTAxTVFpT2l6ZzJUQk5oY2xEV3k1UjJvYU8rb0lSOFdJVEtKZ3BMYTNBTGpSSS9XcEJmQzY2cTd2SXgvRzA2MzFKc1FTNjBUeFRydEpobWIvcWtpb2ZWdW5sV3VQaGd0Sk1CbUt6VUVQeStiRkVDQUZUNi9XMHlkV0tNdFR0L1BmdjFYcjhLQWFCVllIYTk5VUI2RXd6dTdGbWtHQ2RpWlJOYm82K1E1Qk43TnhOUFlDM0FJT05FbnBTTkQ4UUNuczFiTlRsbmRwU3diUG9nVTFhcjE1SW1uQ1VpTzlVcUF3YWxQOWZWWWQrZGo1Zzl6NUIwNzA3L2Y3akwrUkdJci82Z09uTTJ2SnpKMC9FdTdNRWZFRS9oc2JDTVJ3d2RwNzJQRFhraXRZSjRLTHhLREZMVG13NUswUXBNbUQrQ1VHUHp1UkEwaEM3NjFhSXNKVW5VOUdtQ1lCRUNwSVBRODN5SExvVVlWWnQ3UHZZSnhyeS81dGZkclhWYjY5RTI2SndibXNzT1hXZTAzQ1ZIblJpZ2NBc2NydFJBZnUwYXhlRWZodVVZZ094T1BXQWxQbzFERnF3LzkyMlg2aFp0NzJ4WXZsMGVNU05KRktBUkFEYzZxR09FYmRoeTVjS3FRdHRUeTFsWlhWdGJWN25PREV3M3lZSTdKOU8vbEdPUGJBUVFiblh6TE0yck8wY0tueXpTVTh6OCtGVm0rUVpMOTVodnNKZUg2dWdhNGdaMDlxdlNBdWVpK3BCbFV2UllDTkhTYmUwV1VsN2RTWDhtaGtoZWFqTTNJeHFXbW1Ocjh4ZHpMZEcyOGYrdXAxMDkwS0Vnd3VzODdVMk9OTVZTenVMdy9ta1NqeDVNL0JQNUk2ZjBDMVVqT05qTWFDWWVNWmRFY2J5NzlzbjQyaHVlQ2pQdWpKemtsYktxMVVXQk01NGpHMUlPVEhXYVpsaHB5dXNXMU9ObFFFaHVaMjQ2ajhiYnVDNWZEbVZEeVBLZTZVN2xVWExDSTFVdDltZVBId1B2MkVabzhRMHJkc2xKdGRYaVRKWGRid2l1WmVESlJKSjE2b1BGVWZCSUZUS1FPbnFPTVdVa0VTZS9QTFJIQ0ZzS3phVUVQWXhFczgyWlpOYXlZRU5LYTlqcVBrWnEwSUxDSS9OM3R1M0ZvbXBnUzFFRW1DRUpBVm5MdlJIdWNHYW05SE5lZnoxd2F2RktUL1l4MDdGakpkTGhDc2c4ZlF0RkYrRWwrWHlqTjVzSkFxenl1VDUxM1Ard1BxRUhNajVrdGNaZ2NwYUVpalF5V2p0L3RzT2N2VVh0bVdFUGw4dXhLZHNpOUU5Q2N3bmtzV0N5d2c2REI4SlFqRU55RUpCYUNaenNhQ0I1ZjRUa2tqZWlacHM3MXQ4eEUxQWk5SHR4YXJJZGswYUtiUy9RYXNBT1BlYXI2ZlUwUWNqYldBSElSL3lvN2ovZVFENzExdVAya1BSOUp2elh3REN4NzdUeTBNSGRiS2U4MUhFV3hoZGRici8yVjFKck5YeFVQUHBFdDhRRW1COUMraDFKQUM3Vm4wTVZ3QjJQdVNReS90dXAvb24ycnVlb1VaMno2K0VQeE1KUmU4dzllWkNsL1hxMHdINGZNczkraktlYjh3UGNwNVNHR3hJZHUwOHRicHRJL0g2a0VOSi9pcDIxZWVKYm5OSHFXVDdBYU0wdGxhM2hyNmZoMlljRE5ZVlJ6Z0VlTml1WjRLc0h0NXo5dUFWNDQ2bkZ3dG8zUU5FaEFuT1hKRGdzN3dpMzlwdndLR0JLdzdsWFJ2VVFwZndqaEp1NXZ5K3lsVSt5TEdQQ2dhdXFCL2lZU2NpelVrZlBtd0JuYnVSWWJ5SElEMGlkUFpQZXJ1OUlkOUFrZTg5d1Y0eEE2K0t4ckk1VWdtS21mSW50SmJZWTlIbURtbWJzcCtBRVZNTDBIYVg4ZzQ3REM5ZWNSclVHUWd1WHd0VlJOdTA1MGhQNWZ1bENmVzVxSzE3c3dISHRMa1RxNEltcDNnVVR5L0Nrcmg3V2hnWHdvM01iSkxGdlpSeFJUNVdKS1A3MzlFVTN1dHBqTnphelc4UHZNZVJWbXBqTFRXd21XWnFTY3oyL01uY2loZE5vajRZcDF5TVZvQWgzU3dwVDY1c2lhYVdzNjFSMUpiaFJJcWVxNVBLUXFHVEhUaXZNOGpRVlhRUjdmc1F4QkR3TC9aV0dHQm5pQ3RkVXRFM2NjRytKTzlMMHVJcVlRLzRBb09pREV4ZGIwUitvSHJyREhvRXNiMHFUbjZjVWMybndGVU5ZRTZVa1lhL2xERjVFcURSN2xzZzZCKzNDcmM0Q0hkSlNVYU1SS3p2dG9scW1xMGU2RjlmS3Q3QUlXQUVoTkVucStRY3h4dG1yUHJ3TkJXa0dKdWkvYXhtVDJvNVI5ZWpJWm5raE04Smlla1Y2Ly92b1hZcWNWVllaTmpWYkdkZzZYZkJGeW1BWjNMS1VjZzRLY2Z5dzlXNEZSQzZVc0NNanlaZ201aFB1ajVydWhBNUFKblUxbTJ0N3F3RnQ1ZTZRaHZuVmZpNE9SaEVlZXRteUsyL1U3U2tySFBVUmlqaGRMSi8zTlZSVjdtSE9ZYnlrRldtRWlQSVZ2T2M2YkJjN1NIcGFJK3JJc0xObDcyT3A2TTJXbjBkWjNPRDc5bGdjS1VlNWlWYkhnYUF1ZC9ORmZiSzJUSGxSVHdDUkVzcFdFRWZ1dlVma09oRW1qTHRzNytjY0ZqYkpoVEEvc21lRGN2M2E1dzJzaHRrY3lrYW5LNnRQL0RUaE5ZWjVTWUNLQmxJNDh3NUdLUlpGejNqUUpISjFieTgvbldWVGI0U2l2WEUza1F6TzBSU0ZjVFNBTHhRT1dKMnVXbUlYSkNqbytsQWVCS0R4c1Jlekh0T0Q5MW9jN2xMOVVjMkdBeTAxYitRMVNxdFVURzhkaGRrUkZUMTF0Zjh1UEZEUFVNNm4xWFBzNndvRnFPNmRuRE0xWTgxNlJ5aEJkN1R5T0xjcnhOYXBQVThpQ3ZMV3BaNWJRcVkyQi9TbGxQYnpjVnRaQ3FIa3AxMFIvcWhyS1V5RVZuMHpiMEd3RThpS1d1T2pZMUFsTkR0TitTRTZUVC9aQlVYQkdKUFU3MjJRUE56V0RyRW5ia1hGRTd3cjkydGNBUE1DMDE2YktEWXFsMHYyV051RXNJVzVtVHo3T2xNM240VUM5NWtUR1J3bHpyeDNSTm1FYTJmTS9CYnd3Uk9FVmhkYUNyN0lCSEI3NXRtY2crcUFzV1huWGpyQ3B4ZW5DdENkUytWTWdMKzIySVppUmxFNkVWY2tadkRETFFHaGpBalRkUnJudHJBK1ZEYVk0aGNFZWREQy8waE9zRUw5M0h3dE9KVEtVVkdYbmZVVmxoZVlUbnlhcnZmZHV6aWYySlZJYkFpdHBqKzNvQmNiTjJPNkNwN1UwTDZvbWFZZGZtaC94cUtrUyszNlpzb3JWWHIxM2p0S0lRSmswMHU4OVJGbnhhYWROZDJKbjE4bTdVN0xqaG9RZmNpNDl3NnFQL0s1bWZJc2J2dFAxV3ZQRzVuV3ZreGJKSnJqRzJNSWd4dVVYV1IwQUN0Q0ovOFJOdEhqZC9mcGRCbG5yWCtGajRwMHoxd2plSXZheHRCVEtadmRySlZBUWllckFKRS9TZXdXRy9aRm1YaE1kdkpQNmxGMExIeHhtUkxCZW1OcEhsUnJiYkxHU04rT1MrVHpGTDBpcDVKWm1NOHFwdHdBT1lJbFJyeWZkQjg4eXNnZDBqcGFPSVRhQm1qM292U01OVW1zV3lHWUJSellLdEg0ZmJJakU0YWE4SUdXMFBuVWpUeVlQcnI5bGJ4cFFTMmhVK1JnWGIrR1c3L29SSlpHMU9RRkhqNnRYVHV6RmxoWEV6TlpjQ0N3OUpnS0NXQXlHM2FaTUsydk52S0pQZUJVQzJZalg5bkxSQ2VVYUhPaTkyV1ppQnlrTEdGbFdFNnAydVBQamYyczVQN2ZKVTJKcXltUHZQemo3Qmhpb1RQTkhBU3lhckphTTZZT2FvOXJrZGhCREVsQ25wRHFtRzNvSVd6SEZxZ2gza2xScVpiS3V3THhKcTh6TTNub2daZ1pON3BScXpqd24vNkY2V05OaHc2blgvMzdvMCt3cXl4WmJLcXZ1a3pmVXFlTElDVU1Tams0ekRkUVB6SzcyOUlpazQ2TCt2aFBRdHlaRUpQcFB2bmdwZWpmbXRiL2J0eXJFTzViY0lzaE16UHYvYlpkWEJiQ3RFL1lHVUF5aklKMitCQ0tKaTFQd0lVN2N3eEV5MTBFYkxUbEY1cVZaZjgvM3Bqd1lxT01QbGtDUXlOSUNPUWpoajUwQS9FMmpMeFRlRVAzN2xnazhybVRLdENQZU5jU25HcldMRElVMlo3VXRBYVRleS96NjIxMURJb3hLcHBFNEp3alZDcytvMDROZVgzSmczQUI2NWRpYnNqM3BSQjZZSEwzSWVZc3BKOGlkbDhIbWMrMzFubXlrOUEzeEgySGg3VFRaTkVOZkx0K1RPNnVXYnczbHFWYmEza1h2UEZYcGdrSHc0dEJCdjZSMVQwQnVldCs2R29IR0k3YnVzWTZyckJ3TEY1cDhidWxkRmNvTWFvWDc2YlVKUnNKb2QrTUNicVRlQ3p0NCtVc3NZWk5haDR5NFE1TmoxQmVrMDB3Ui9tdEdPei9iejlzR3gvQng4djJwZ1B1RUMzVldZRzE3bitpaGlLaExVaGdRVlN6OWVVdWVhM1E4M01DMFQwUytqS2VGMWV1NXUzTDRVc051MmFZT2V3TmdmSVdqakY2dHg2NkM4SUR1Z1Fwc3BzNWlyaDZPRWcvdFhWbVVIV285TW1mTGFiOThDZFdzV2dCZnFSVUNxYTgrcldlMTlEWkw0aFlXZFZBUG8wSjBlSW53dXhxSjdUU0ZjbzNoV3JGVjE5eDZjUWtFeEtYVUlXQzdwMWVTRkM0MXpKRWVONVpReXk0NTdISi9mK0o4R2ZTUXlRTk1XOGVUZFNHWndEbkgxZGpLcDlLaVoxczhqdGN4bXNpcU1xMVlQeHFCanZjVUVZSlkxb2l1aEd0dUM3d3ZSdjU1VDZEN2VWbTdja2M0R1N2VW9reXo2Ty84NmF4YU4wY0ZjVWhyczljVnBubzVtMzA2V2gzZW5kMXRVaVV2UWdIT1F0dE1KbE5oMEdzQk9CV1ZETjZ5TzV0c09tNXZTOFRrbDgyeVZIdVBtb0tZUzBweWN5TW5wRTdGTllyOHhVRy9zNUJ1Tk15VnZTOWpaWVg4TWdJYXEwdElGNHZJcnplZERCRDlHbTQyd3NmeXlpN01ZRjE1cWlhVDR0TkE0T3pUS3JTYWtydkhRR21qUTA2akx2bUl3bW94bTl0bk9ndk85YjYwQlFXaXFzcGZpUXdGVFBjYkU3ak5qTXFQNFIrQ2wwU2pvbDNHRFVUUkIyczNlT20vajc2NE8xQU1TbGdzYnltQkRML25TUkZYck96TVBOaFptNlRDWW83aUcxOUN2L1o3OTkxWkFqWXZWdUc1bUc3bFBNb0MxTkk3SlVVRldCcDRHeW9PWXlYVVVIRDltRGU1Q0NnallPUW9UUWo0QXh3VXkzaHRWY1JoNU03b2tnSW9IYVFDMDFnQ1htMkRTQ0t5cnZBY1p5dmxCRmFrZHFIdkY2eEc2L1NBU3ZDT1ZNVFc3c2JsNGpQRDBEY1pTaVlRM2htdUpLL1lZTnNCMTJBU0hWTnBsazRGUDIvM290aFhSajE0VjBLVVV4NCtIbUZSUm5nMTUyZDZRNUlGUEZhb0M1ZkpFTnhOYzh5ZDBteEg0cGFYVU5EbEJLNHU5MVBFZVhQb082S20xM0pKZ2k5dGxZTUZDZy9oK0ZqVzZadHBESGswSURLQ0txMEh1bDRCVERpdWpRM09zQTJyaElZT3oucTVCQWw5ZmxPaTg3Ul9Yd3hBOTdmOHE2bGR0Vm0taHJ2bjRSVlhuTmlpSUxFSmJtMjN0bkprQU1KN0RnYklZV3lhclc5VUsxWUtmSm5vVklwbnZaMHc=",
                "failN": "0",
                "geolocation": "",
                "mfaState": "",
                "password": password,
                "rememberMe": "true",
                "submit": "Login1",
                "username": username
            }

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://sso.jvtc.jx.cn",
                "Referer": "https://sso.jvtc.jx.cn/cas/login?service=https%3A%2F%2Fmicroserver4.jvtc.jx.cn%2Fcas"
                           "%2Floginapp%3FtargetUrl%3Dservice%252Fsignin%252Fxqindex",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
            }

            response = requests.post("https://sso.jvtc.jx.cn/cas/login", params=params, data=data, headers=headers,
                                     allow_redirects=False)

            tickets = response.headers['Location']  # 未经处理ticket
            ticket = tickets[tickets.index('ST'):]  # 传递给下一段处理后的ticket
            print("▃▄", end='')

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
            print("▅▆", end='')

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
            print("▇█")

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
            response = requests.get("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/getsignin",
                                    headers=headers,
                                    cookies=cookies)  # 打卡结果

            if len(response.text) > 550:  # 判断返回数据长度以判断是否打卡
                today_signdata = eval('{' + response.text[27:])  # 当天是否打卡
                today_location = today_signdata["data"]['signin']['location']  # 今天打卡位置
                toda_signtime = today_signdata["data"]['signin']['updateTime']  # 今天打卡时间
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
                    "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 "
                                  "MQQBrowser/6.2 TBS/045738 Mobile Safari/537.36 SuperApp",
                    "X-Requested-With": "com.supwisdom.jvtc",
                    "Sec-Fetch-Site": "same-origin",
                    "Referer": "https://microserver4.jvtc.jx.cn/h5/pages/service/signin/xqindex",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cookie": "userToken=" + idtoken + "; Domain=microserver4.jvtc.jx.cn; Path=/; " + "JSESSIONID=" + jsessionid

                }

                response = requests.post("https://microserver4.jvtc.jx.cn/api/blade-signin/signinlog/submit",
                                         json=payload,
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
