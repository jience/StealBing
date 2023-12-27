# -*- coding: utf-8 -*-

import os
import win32api
import win32con
import win32gui
import urllib3
from urllib.request import urlopen
from PIL import Image


class StealBing:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.url = 'https://cn.bing.com'
        self.bg_image_name = ''
        self.bg_image_url = ''
        self.local_image_dir = r'C:\\Users\\zhangxiaojie\\Pictures\\Windows 11\\Wallpaper\\'
        self.local_jpg_filename = ''
        self.local_webp_filename = ''
        self.is_remain_bmp = False

    def parser_image_url(self):
        r = self.http.request('GET', self.url)
        temp = r.data.decode()
        temp = temp[temp.index('background-image: url(&quot;/') + len('background-image: url(&quot;'):]
        temp = temp[:temp.index('"')]
        temp = temp.split(".webp")[0]

        self.bg_image_name = temp.split("id=")[1].split(".webp")[0]

        # 1080p的图片替换为UHD超高清格式
        self.bg_image_name = self.bg_image_name.replace("1920x1080", "UHD")
        
        self.bg_image_url = self.url + temp.encode('utf-8').decode("unicode_escape")
        self.bg_image_url = self.bg_image_url.replace("1920x1080", "UHD") + '.jpg'
        print(self.bg_image_url)

    def create_local_filename(self):
        self.local_jpg_filename = self.local_image_dir + self.bg_image_name + '.jpg'
        self.local_webp_filename = self.local_image_dir + self.bg_image_name + '.webp'

    def download_image(self):
        if self.bg_image_url == '':
            self.parser_image_url()
        if self.local_jpg_filename == '':
            self.create_local_filename()
        r = self.http.request('GET', self.bg_image_url)
        w, h = self.get_image_size()
        if w > 0 and h > 0:
            self.local_jpg_filename = self.local_jpg_filename.replace("UHD", "{}x{}".format(w, h))
        with open(self.local_jpg_filename, "wb") as fd:
            fd.write(r.data)

    def get_image_size(self):
        width, height = 0, 0
        im = None
        try:
            im = Image.open(urlopen(self.bg_image_url))
            width, height = im.size
        except Exception as e:
            print(str(e))
        finally:
            if im:
                im.close()
        return width, height

    def webp2jpg(self):
        im = Image.open(self.local_webp_filename)
        if im.mode == "RGB":
            im.load()
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
        im.save('{}'.format(self.local_jpg_filename), 'JPEG')
        if not self.is_remain_bmp:
            os.remove(self.local_webp_filename)

    def update_bg_image(self):
        img = Image.open(self.local_jpg_filename)
        img.save(self.local_webp_filename)
        os.remove(self.local_jpg_filename)
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.local_webp_filename, 1 + 2)


if __name__ == '__main__':
    stealBing = StealBing()
    stealBing.download_image()
    # stealBing.webp2jpg()
    # stealBing.update_bg_image()
