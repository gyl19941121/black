from winreg import *

'''
从注册表中检查MAC地址

'''

def va12addr(val):
    addr = ""
    for ch in val:
        addr += "%02x "%ord(ch)
    addr = addr.strip(" ").replace(" ",":")[0:17]
    return addr

def printNets():
    net ="SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged"
    print (net)
    key = OpenKey(HKEY_LOCAL_MACHINE,net)
    print ("\n[*] Networks You hace Joined.")
    for i in range (100):
        try :
            guid = EnumKey(key,i)
            netKey = OpenKey(key,str(guid))
            (n,addr,t) = EnumValue(netKey,5)
            (n,name,t) = EnumValue(netKey,4)
            macAddr = va12addr(addr)
            netName  = str(name)
            print ("[+] "+netName + "" + macAddr)
            CloseKey(netKey)
        except:
            break

def main():
    printNets()

if __name__== "__main__":
    main()