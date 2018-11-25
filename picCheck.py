
import optparse 
from PIL import Image
from PIL.ExifTags import TAGS
import urllib.request,urllib.parse
from bs4 import BeautifulSoup
from os.path import basename

def findImages(url):
    print("[+] Finding images on "+url)
    urlcontent = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(urlcontent)
    imgTags = soup.find_all("img")
    return imgTags

def dowloadImages(imageTag):
    try:
        print("[+] downloading image..")
        imgSrc = imageTag("src")
        imgContent = urllib.request.urlopen(imgSrc).read()
        imgFile = open(imgFileName,'wb')
        #print (imgContent)
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        return ""

def testForExif(imgFileName):
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        if info:
            for (tag,value) in info.items():
                decode = TAGS.get(tag,tag)
                exifData[decode] = value
            exifGPS = exifData["GPSInfo".encode(encoding="utf-8")]
            if exifGPS:
                print ("[*] "+ imgFileName +"contains Gps metadata")
    except Exception as e:
        print(e)

def main():
    parse = optparse.OptionParser("usage%prog -u<target url>")
    parse.add_option("-u",dest = "url",type="string",help = "specify url address")
    (options,args) = parse.parse_args()
    url = options.url 
    if url == None:
        print (parse.usage)
    else:
        imgTags = findImages(url)
        #print (imgTags)
        for imgTag in imgTags:
            print (imgTag)
            imgFileName = dowloadImages(imgTag)
            testForExif(imgFileName)
    
if __name__=="__main__":
    main()

