#-*- coding:utf-8 -*-
#进行PDF元数据的分析，查看对应的PDF的信息

import optparse
import PyPDF2
from PyPDF2 import PdfFileReader


def printMeta(fileName):
    pdfFile= PdfFileReader(fileName,'rb')
    docInfo =pdfFile.getDocumentInfo()
    print ("[*] PDF MEtaData FOr "+str(fileName))

    for metaItem in docInfo:
        print("[+] "+metaItem+":"+docInfo[metaItem])

def main():
    '''
    parser = optparse.OptionParser('usage %prog '+"-F <PDF File name>")
    parser.add_option("-F",dest = "fileName",type = "string",help = "specify PDF file name")
    (options,args) = parser.parse_args()
    fileName = options.fileName
    if fileName == None:
        print (parser.usage)
        #exit(0)
    else:'''
    
    printMeta(fileName="UserManual.pdf")
        
if __name__ =="__main__":
    main()
