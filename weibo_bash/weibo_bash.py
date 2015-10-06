#!/usr/bin/env python3
#coding:utf-8
__author__ = 'zhuzhezhe'
'''
功能实现:命令行下发布微博,获取最新微博
'''
from weibo import Client
import  getopt
import sys
import configparser

versions = '0.1'


# 写入用户数据
def write_data(uname, pwd):
    conf = configparser.ConfigParser()
    conf['config'] = {}
    conf['config']['username'] = uname
    conf['config']['password'] = pwd
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)
    print('写入成功')


# 读取用户数据
config = configparser.ConfigParser()
config.read('config.ini')
username = config['config']['username']
password = config['config']['password']


# 接入新浪接口基本信息
api_key = '3842240593'
api_secret = '93f0c80150239e02c52011c858b20ce6'
# 默认回调地址
redirect_url = 'https://api.weibo.com/oauth2/default.html'


# 登陆验证
c = Client(api_key=api_key,
           api_secret=api_secret,
           redirect_uri=redirect_url,
           username=username,
           password=password)


# 最新微博
def new_weibo():
    try:
        data = c.get('statuses/friends_timeline')["statuses"]
        for i in range(len(data)):
            print("用户:"+data[i]["user"]["screen_name"])
            print("微博:"+data[i]["text"])
            print("\n")
    except Exception as err:
        print(err)
        print('确保已完成登陆.请填写用户名和密码.')


# 发布微博
def add_weibo(words):
    try:
        c.post('statuses/update', status=words)
        print("发布成功!")
    except Exception as err:
        print(err)
        print('确保已完成登陆.请填写用户名和密码.')


# 用法
def usage():
    text = '--------weibobash使用帮助--------\n' \
           '-h<--help>:  显示帮助信息\n' \
           '-u<--user>:  输入用户名和密码\n' \
           '-n<--new>:  显示20条最新微博\n' \
           '-a<--add>:  发布一条微博\n'
    print(text)


# 主程序
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hna:vu", ["help", "new", "add=", "user"])
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
        elif o in ("-u", "--user"):
            user = input("请输入用户名：")
            pwd = input("请输入密码：")
            write_data(user, pwd)
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()


