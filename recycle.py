import os
from winreg import *
import optparse
'''
检查注册表中，回收站被删除的人的信息和文件
需以管理员身份运行

'''

def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList"+"\\"+sid)
        (value,type) = QueryValueEx(key,"PrfileImagePath")
        user = value.split("\\")[-1]
        return user
    except:
        return sid

def returnDir():
    dirs = ["C:\\Recycler\\","C:\\Recycled\\","C:\\$Recycle.Bin\\"]
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

def findRecycle(recycleDir):
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        files = os.listdir(recycleDir+sid)
        user = sid2user(sid)
        print ("\n [*] Listing Files For User: "+str(user))
        for file in files:
            print ("[+] Found File :"+str(file))

def main():
    recycledDir  = returnDir()
    findRecycle(recycledDir)

if __name__ =="__main__":
    main()
