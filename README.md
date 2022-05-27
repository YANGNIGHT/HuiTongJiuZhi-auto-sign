# 九江职业技术学院 慧通九职打卡平台自动打卡脚本



## 说明

**本打卡脚本仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。**

## 更新记录

- 2022.5.25： 本地打卡程序完成，实现单人本地打卡
- 2022.5.26： 实现邮箱推送功能，实现多人登录
- 2022.5.27： github action 自动运行

## 使用方法

0. **写在前面：请在自己fork的仓库中修改，并push到自己的仓库，不要直接修改本仓库，也不要将您的修改pull request到本仓库（对本仓库的改进除外）！如果尚不了解github的基本使用方法，请参阅[使用议题和拉取请求进行协作/使用复刻](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/working-with-forks)和[使用议题和拉取请求进行协作/通过拉取请求提议工作更改](https://docs.github.com/cn/github/collaborating-with-issues-and-pull-requests/proposing-changes-to-your-work-with-pull-requests)。**

1. 将本代码仓库fork到自己的github。

2. 根据自己的实际情况修改`data.json`的数据，参看下文。**开发者不保证这些模板的正确性。**

3. 将修改好的代码push至master分支。如果不需要修改 `data.json`，请在 `README.md` 里添加一个空格并push，否则不会触发之后的步骤。**请在自己的仓库中修改，不要pull request到本仓库！**

4. 点击Actions选项卡，点击`I understand my workflows, go ahead and enable them`.

5. 点击Settings选项卡，点击左侧Secrets，点击New secret，创建名为`STUID`，值为自己学号的secret。用同样方法，创建名为`PASSWORD`，值为自己中国滑稽大学统一身份认证密码的secret。这两个值不会被公开。

   ![secrets](imgs/image-20200826215037042.png)

6. 默认的打卡时间是每天的早上7:30、中午12:30和晚上19:30，可能会有数分钟的浮动。如需选择其它时间，可以修改`.github/workflows/report.yml`中的`cron`，详细说明参见[安排的事件](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#scheduled-events)，请注意这里使用的是**国际标准时间UTC**，北京时间的数值比它大8个小时。建议修改默认时间，避开打卡高峰期以提高成功率。

7. 在Actions选项卡可以确认打卡情况。如果打卡失败（可能是临时网络问题等原因），脚本会自动重试，五次尝试后如果依然失败，将返回非零值提示构建失败。

8. 在Github个人设置页面的Notifications下可以设置Github Actions的通知，建议打开Email通知，并勾选"Send notifications for failed workflows only"。

## 在本地运行测试

要在本地运行测试，需要安装python 3。我们假设您已经安装了python 3和pip 3，并已将其路径添加到环境变量。

### 安装依赖

```shell
pip install -r requirements.txt
```

### 运行打卡程序

```shell
python auto.py
```
其中，`[DATA]`是存放打卡数据的json文件的路径，`[STUID]`是学号，`[PASSWORD]`是统一身份认证的密码明文。



