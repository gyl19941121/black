import logging
import subprocess
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import *

if len(sys.argv)!=2:
    print ("usage - ./arp_disc.py [interface]")
    print ("Example- ./arp_disc.py eth0")
    print ("Example will erform an ARP scan of the local subnet to which eth0 is assigned")
interface = str(sys.argv[0])
ip  = subprocess.check_output("ipconfig " + interface +"| grep 'inet addr'|cut -d':' -f 2 |cut -d '' -f 1",shell=True).strip()
prefix = ip.split('.')[0]+'.'+ip.split('.')[1]+'.'+ip.split('.')[2]+'.'

for addr in range(0,254):
    answer = sr1(ARP(pdst = prefix+str(addr)),tiemout=1,verbose=0)
    if answer ==None:
        pass
    else:
        print (prefix+str(addr))