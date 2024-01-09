# automatic_login_Drcom
这是一个Python写的校园网自动登录程序,适用于Dr.COM校园网认证系统,以模拟GET请求的方式完成登录验证
您可以直接下载免安装版使用[点我下载](https://github.com/heiyebaitian/automatic_login_Drcom/releases)

## 环境
* python版本为3.7及以上(低于该版本未测试)
```
conda create -n name python=3.7
```

* 所需依赖
```
import requests # GET请求使用 
import time # 时间戳
import random # 随机生成字符串
import string # 字符串处理
import socket # 获取IP地址
import sys

```
* 依赖一键安装命令
```
pip install -r requirements.txt
```

## 使用说明
#### 第一步:安装Python
您可以前往 [点我下载](https://www.python.org/downloads/) 安装对应的Python环境
此处不对该步骤做过多阐述,详细教程参见 [安装教程](https://zhuanlan.zhihu.com/p/104502997)
#### 第二步:执行登录信息配置程序
请先打开 `终端程序`
使用 `cd` 命令到您存放 `main.py` 的路径中
输入以下内容运行本程序
```
py main.py
 ```
 首次执行本程序可能会出现以下内容,请按照提示完成输入即可。
 ```shell
  PS D:\Python Project>py main.py
 检测到您可能是第一次使用!
请按照以下提示创建登录信息:


请输入您登录服务器的IP地址(带端口号):************:801

请输入您的登录用户名:********************

请输入您的登录密码:******************

您是否要自动生成一个新的PHPSESSID?(Y/n)Y

已为您创建一个新的PHPSESSID:******************

登录信息配置程序已完成,请重新执行本程序以开始登录!
 ```
 #### 第三步:登录测试
 ~~请先退出您的校园网,并再次使用以下命令执行本程序~~
(2023.9.3版本更新后已无需手动推出校园网,程序会根据情况自动重置登录)
 ```
py main.py
 ```
 如果出现以下内容,则代表您已正确配置登录脚本
```shell
PS D:\Python Project> py main.py

请求URL为:
http://**********************:801/eportal/?c=***************************


服务器已应答
dr**********({"result":"1","msg":"**************"})

登陆成功!
登录有效时间为24小时
```
 #### 第四步:自动登录
 以Windows为例,您可以创建一个`.bat`文件写入以下内容
```
cd D:\Python Project  #路径设置为您自己的
py main.py

```
然后将此`.bat`加入Windows触发器进行定时执行或开机自启等一系列操作
具体教程参照 [点我查看](https://blog.csdn.net/m0_46629123/article/details/120070320)

## 注意事项
> 1. 本脚本并不适用于所有校园网登录系统,您可能需要根据自身环境情况修改
> 2. URL合成步骤中,wlan_user_ip、wlan_user_mac、jsVersion等参数的可能要根据自身情况测试,您可以使用浏览器F12来抓取
> 3. 请确保您使用本脚本符合校方规定,由于使用本脚本造成的一切不良影响由使用者自行负责
> 4. 欢迎您对本脚本进行优化,并上传适用于您自己学习的脚本 :smile: 
> 5. 注意,登录配置信息没有采取任何加密手段,请注意保护您的个人信息安全!!!

## 常见错误提示
1. 如果提示`主机IP地址`类错误
这可能是因为您的主机IP地址不合法或已被其他设备使用
不合法的原因通常是因为您外接路由器,使用代理程序导致的,请手动将`host_ip`变量设置为正确的IP地址
被其他设备使用,往往是因为您将`host_ip`变量设置成了静态参数,请将`host_ip`变量设置`get_lan_ip()`以自动获取IP地址
2. 如果提示登录信息错误(包括账户密码错误)
请手动删除执行目录下的`login_information.inf`文件,或手动或修改`login_information.inf`文件的登录参数
2. 如果打包版执行时,控制台一闪而过,可以直接在终端执行以查看日志

