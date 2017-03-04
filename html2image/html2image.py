#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This is a XXX script.
What is the function of this script? """

__author__ = 'GZhY'
__version__ = 1.0

from selenium import webdriver
from PIL import Image
import io
import time
import JSInjection


class Html2Image:
    def __init__(self, url, jsCode=None):
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1200, 900)
        self.browser.get(url)
        self.jsCode = jsCode
        self.image = None

    def getImage(self):
        if self.jsCode is not None and isinstance(self.jsCode, JSInjection.JSCode) and self.jsCode.getJSCode != "":
            # print(self.jsCode.getJSCode())
            self.browser.execute_script(self.jsCode.getJSCode())
            for i in range(30):
                # print(self.browser.title)
                if self.jsCode.finishedSign in self.browser.title:
                    break
                time.sleep(10)

        self.image = self.browser.get_screenshot_as_png()
        # self.browser.close()
        return self.image

    def getElementImage(self, cssSelector):
        if not self.image:
            self.getImage()
        element = self.browser.find_element_by_css_selector(cssSelector)
        left, top = element.location['x'], element.location['y']
        right = left + element.size['width']
        bottom = top + element.size['height']
        im = Image.open(io.BytesIO(self.image))
        im = im.crop((left, top, right, bottom))
        # im.show()
        imgByteArr = io.BytesIO()
        im.save(imgByteArr, format='PNG')
        return imgByteArr.getvalue()

    def saveImage(self, image=None, filename="result.png"):
        if not image:
            if not self.image:
                image = self.getImage()
            else:
                image = self.image
        try:
            with open(filename, 'wb') as f:
                f.write(image)
        except IOError:
            return False
        finally:
            image = None
        return True

    def __del__(self):
        self.browser.close()


if __name__ == '__main__':
    h2i = Html2Image("https://www.baidu.com/", JSInjection.Scroll2Bottom())
    h2i.saveImage(h2i.getImage())
    h2i.saveImage(h2i.getElementImage("#head > div > div.s_form > div"), "element.png")
