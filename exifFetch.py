import urllib2
import optparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS
import os

def findImages(url):
    print '[+] Finding images on ' + url
    urlContent = urllib2.urlopen(url).read()
    soup = BeautifulSoup(urlContent, "lxml")
    imgTags = soup.findAll('img')
    return imgTags

def downloadImage(imgTag):
    try:
        print '[+] Downloading image...'
        imgSrc = imgTag['src']
        imgContent = urllib2.urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName, 'wb')
        imgFile = write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        return ''

def testForExif(imgFileName):
    # as of March 2017 this technique is completely bugged.
    # however manually running exiftool still returns data
    # gonna use a os.system command to manually run it against it as a hacky solution
    #
    # try:
    #     os.system('exiftool %s') % imgFileName
    # except:
    #     print 'No exif information has been found'
    try:
        exifData = {}
        imgFile = Image.open(imgFileName)
        info = imgFile._getexif()
        # with exiftool.ExifTool() as et:
        #     info = et.get_metadata_batch(imgFile)
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value
                exifGPS = exifData['GPSInfo']
            if exifGPS:
                print '[*] ' + imgFileName + ' contains GPS MetaData'

    except:
        pass

def main():
    parser = optparse.OptionParser('usage%prog ' + '-u <target url>')
    parser.add_option('-u', dest='url', type='string', help='specify url address')
    (options, args) = parser.parse_args()
    url = options.url
    if url == None:
        print parser.usage
        exit(0)
    else:
        imgTags = findImages(url)
        for imgTag in imgTags:
            imgFileName = downloadImage(imgTag)
            testForExif(imgFileName)

if __name__ == "__main__":
    main()
