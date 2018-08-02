# coding=utf-8
from selenium import webdriver
from actions import *
from models import *
import os

browser = webdriver.Chrome()

if __name__ == '__main__':
    with open('../zhihu_login_info.txt') as f:
        username, password = f.read().split('\n')
    robot = Robot(
        Open('https://www.zhihu.com/'),
        Click('登录'),
        Input('手机号或邮箱', username),
        Input('密码', password),
        Click('登录', choose_func=lambda elements: elements[-1])
    )
    robot.setup(browser)
