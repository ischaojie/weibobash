#!/usr/bin/env python3.4
#coding:utf-8
__author__ = 'zhuzhezhe'
'''
功能实现:命令行下发布微博,获取最新微博
'''
from weibo import Client
import  getopt, sys

versions = '0.0.1'


# 接入新浪接口基本信息
# username = '2712028096@qq.com'
# password = 'wasd1995,./'
api_key = '3842240593'
api_secret = '93f0c80150239e02c52011c858b20ce6'
# 默认回调地址
redirect_url = 'https://api.weibo.com/oauth2/default.html'


# 登陆验证
def login_weibo():
    c = Client('3842240593',
            '93f0c80150239e02c52011c858b20ce6',
            'https://api.weibo.com/oauth2/default.html')
    print(c.authorize_url+'\n')
    print("请打开该网址完成授权,授权完成后请将浏览器地址栏链接中?code=后面的文字进行复制.\n")
    codes = input("请输入code值:")
    c.set_code(codes)
    return c

token = login_weibo().token
c2 = Client('3842240593',
            '93f0c80150239e02c52011c858b20ce6',
            'https://api.weibo.com/oauth2/default.html',
            token)

# 最新微博
def new_weibo():
    try:

        data = c2.get('statuses/friends_timeline')["statuses"]
        for i in range(len(data)):
            print("用户:"+data[i]["user"]["screen_name"])
            print("微博:"+data[i]["text"])
            print("\n")
    except Exception as err:
        print(err)
        print('请确保以完成授权.使用<weibobash -l>.')

# 发布微博
def add_weibo(words):
    try:
        c2.post('statuses/update', status=words)
        print("发布成功!")
    except Exception as err:
        print(err)
        print('请确保以完成授权.使用<weibobash -l>.')

# 用法
def usage():
    text = '-h<--help>:  显示帮助信息\n' \
           '-l<--login>:  用户登陆授权\n' \
           '-n<--new>:  显示20条最新微博\n' \
           '-a<--add>:  发布一条微博\n'
    print(text)


# 主程序
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hna:vl", ["help", "login", "new", "add="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            print(versions)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--new"):
            new_weibo()
        elif o in ("-a", "--add"):
            add_weibo(a)
        elif o in ("-l", "--login"):
            login_weibo()
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()


