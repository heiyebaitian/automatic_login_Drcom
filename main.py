import requests # GET请求使用 
import time # 时间戳
import random # 随机生成字符串
import string # 字符串处理
import socket # 获取IP地址
import sys

# 登录信息创建程序
def create_login_information(): 
    print('检测到您可能是第一次使用!\n请按照以下提示创建登录信息：\n')
    with open('login_information.inf', 'w') as login_inf:
        ip = input('\n请输入您登录服务器的IP地址及端口号（端口一般为801）:')
        user_account = input('\n请输入您的登录用户名：')
        password = input('\n请输入您的登录密码：')
        key = input('\n您是否要启用【兼容模式】（不知道请填Y）（Y/n）')
        if key.lower() == "y":
            compatibility_mode = 1
            print('\n已启用【兼容模式】！')
        else:
            compatibility_mode = 0
            print('\n已禁用【兼容模式】！')
        key = input('\n您是否要自动生成一个新的PHPSESSID？（不知道请填Y）（Y/n）')
        if key.lower() == "y":
            digits = string.ascii_lowercase + string.digits
            random_string = ''.join(random.choice(digits) for _ in range(26))
            cookie = random_string
            print('\n已为您创建一个新的PHPSESSID:'+cookie) # 目测SESSID可能不是必要条件
        else:
            cookie = input('\n请输入您的PHPSESSID：')
            print('\n您的PHPSESSID:'+cookie)
        login_inf.write('')
        login_inf.write('flag = 1\n')
        login_inf.write('ip = '+ip+'\n')
        login_inf.write('user_account = '+user_account+'\n')
        login_inf.write('password = '+password+'\n')
        login_inf.write('compatibility_mode = '+str(compatibility_mode)+'\n')
        login_inf.write('PHPSESSID='+cookie)
        print('\n登录信息配置程序已完成，请重新执行本程序以开始登录！')
        sys.exit (0)
        
# 读取外部IP地址
def get_lan_ip(): # 获取您的IP地址（如果您外接了路由器等情况，会导致本程序无法获取正确的主机IP！请手动在下方host_ip变量修改为您的真实IP）
    ip = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except Exception as e:
        print(e)
    finally:
        s.close()
    return ip




# 登录程序
def login_app():
    try:
        response = requests.get(url_login,headers,timeout = 5) # 发送请求
        print('\n\n\033[32m服务器已应答\033[0m\n'+response.text) # 输出回复报文
        if 'result":"0"' in response.text and 'ret_code":"2"' in response.text: # 重复登陆
            print('\n\033[31m重复登录!\033[0m')
            global retry # 声明全局变量
            if retry == 0:
                print('正在尝试注销并重新登录...')
                retry = 1
                logout_app()
                login_app()
            else:
                print('请检查是否重复登录！\n注意，该错误也可能是因为您的主机IP地址错误导致的，原因可能是您的IP地址已被其他设备占用，您可以手动修改host_ip变量为您的真实IP地址。')
        elif 'result":"0"' in response.text and 'ret_code":"4"' in response.text: # 账号或密码错误
            print('\n\033[31m登录失败!\033[0m\n请检查账号密码是否正确！（请编辑或删除目录下的login_information.inf文件）')
        elif 'result":"1"' in response.text: # 登陆成功
            print('\n\033[32m登录成功！\033[0m\n登录有效时间为24小时')
        else: # 未知报文错误
            print('\033[31m结果异常！\033[0m\n请检查请求内容是否有效或是否被BAN\n常见问题：\n1.您的主机IP地址错误，原因可能是您外接了路由器等情况，您可以手动修改host_ip变量为您的真实IP地址。\n2.您的防火墙拦截了该请求。\n2.您的防火墙拦截了该请求。\n3.您的URL构造错误或URL不属于这个学校的校园网\n')
    except requests.exceptions.ConnectionError as e: # 网络问题抛出异常
        print('\n\033[31m服务器无应答！\033[0m\n连接断开，可能是目标主机不存在或您的网络连接已断开！\n\n', e)
    except requests.exceptions.Timeout as e: # 响应超时
        print('\n\033[31m服务器无应答！\033[0m\n响应超时，可能是目标主机不存在或您的网络连接已断开！\n\n', e)

# 注销程序
def logout_app():
    try:
        response = requests.get(url_logout,headers,timeout = 5) # 发送请求
        print('\n\n\033[32m服务器已应答\033[0m\n'+response.text) # 输出回复报文
        if 'result":"1"' in response.text: # 注销成功
            print('\n\033[32m注销成功！\033[0m')
        else: # 未知报文错误
            print('\033[31m结果异常！\033[0m\n请检查请求内容是否有效或是否被BAN\n常见问题：\n1.您的主机IP地址错误，原因可能是您外接了路由器等情况，您可以手动修改host_ip变量为您的真实IP地址。\n2.您的防火墙拦截了该请求。\n3.您的URL构造错误或URL不属于这个学校的校园网\n')
    except requests.exceptions.ConnectionError as e: # 网络问题抛出异常
        print('\n\033[31m服务器无应答！\033[0m\n连接断开，可能是目标主机不存在或您的网络连接已断开！\n\n', e)
    except requests.exceptions.Timeout as e: # 响应超时
        print('\n\033[31m服务器无应答！\033[0m\n响应超时，可能是目标主机不存在或您的网络连接已断开！\n\n', e)





# 主函数
# 读取配置信息
try:
    with open('login_information.inf', 'r') as login_inf: #读取存储的登录信息到变量
        lines = login_inf.readlines()
        try:
            flag = lines[0].split('=')[1].strip()
        except IndexError:
            print('\n\033[31m发生错误!\033[0m\n登录信息已丢失或已损坏，请重新配置登录信息！\n')
            create_login_information()
        server_ip = lines[1].split('=')[1].strip()
        user_account = lines[2].split('=')[1].strip()
        password = lines[3].split('=')[1].strip()
        compatibility_mode = lines[4].split('=')[1].strip()
        cookie = lines[5]
        host_ip = get_lan_ip() #如果无法获取真实IP地址，请手动设置该变量！！！
        timestamp = time.time()*1000 # 生成符合格式的时间戳
        callback = 'dr'+ str(int(timestamp)) # 合成时间戳（时间戳疑似是不严格校验）
        if compatibility_mode == '1':
            user_account = '%2C0%2C'+ user_account + '%40' # 兼容部分用户名格式
except FileNotFoundError:
    create_login_information()


# 合成登录URL及请求头，如果URL失效了请修改此行格式
# wlan_user_mac、jsVersion啥的可能要根据自身情况测试，您可以使用浏览器F12来抓取URL
url_login = 'http://'+ server_ip +'/eportal/?c=Portal&a=login&callback='+ callback +'&login_method=1&user_account='+ user_account +'telecom&user_password='+ password +'&wlan_user_ip='+ host_ip +'&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=PTXY-Core&jsVersion=3.0&_='+ str(int(timestamp))
url_logout = 'http://'+ server_ip +'/eportal/?c=Portal&a=logout&callback='+ callback +'&login_method=1&user_account='+ user_account +'telecom&user_password='+ password +'&wlan_user_ip='+ host_ip +'&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=PTXY-Core&jsVersion=3.0&_='+ str(int(timestamp))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Referer': 'http://'+ server_ip.split(':')[0].strip() +'/',
    'Cookie': cookie
}
print('\n请求URL为：\n'+url_login) # 输出生成的URL



retry = 0
login_app()
