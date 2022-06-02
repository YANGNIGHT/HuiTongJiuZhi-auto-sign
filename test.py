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