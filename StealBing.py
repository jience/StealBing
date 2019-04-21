# -*- coding: utf-8 -*-

import os
import time
import win32api
import win32con
import win32gui
import urllib3
from PIL import Image


class StealBing:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.url = 'http://cn.bing.com'
        self.bgImageUrl = ''
        self.localFileName = ''
        self.localBMPFileName = ''

    def parserImageURL(self):
        r = self.http.request('GET', self.url)
        temp = r.data.decode()
        temp = temp[temp.index('g_img={url:"') + len('g_img={url:"'):]
        temp = temp[:temp.index('"')]
        
        self.bgImageUrl = self.url + temp.encode('utf-8').decode("unicode_escape")
        print(self.bgImageUrl)

    def createLocalFileName(self):
        randomStr = time.strftime("%Y%m%d", time.localtime())
        self.localFileName = 'F:/Graphics/Bing/' + randomStr + '.jpg'
        self.localBMPFileName = 'F:/Graphics/Bing/' + randomStr + '.bmp'

    def downloadImage(self):
        if self.bgImageUrl == '':
            self.parserImageURL()
        if self.localFileName == '':
            self.createLocalFileName()
        r = self.http.request('GET', self.bgImageUrl)
        with open(self.localFileName, "wb") as fd:
            fd.write(r.data)

    def updateBGImage(self):
        img = Image.open(self.localFileName)
        img.save(self.localBMPFileName)
        os.remove(self.localFileName)
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.localBMPFileName, 1 + 2)


if __name__ == '__main__':
    stealBing = StealBing()
    stealBing.downloadImage()
    stealBing.updateBGImage()
