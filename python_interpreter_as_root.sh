#!/bin/bash
echo 'mypassword' | sudo -S :
sudo -E /usr/bin/python2 "$@"
#用当前用户的密码替换mypassword
#sudo -S从管道接收密码
#:空命令，什么也不做，这一句利用了sudo的特性，只要在第一次使用sudo的时候输入密码，5分钟内都不用再输入
#-E保留当前用户的环境变量
#/usr/bin/python2 替换成你要使用的python命令的完整路径
#“$@”将参数传递给python命令