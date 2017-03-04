#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This is a XXX script.
What is the function of this script? """

import io
import time
import JSInjection
from PIL import Image
from selenium import webdriver

__author__ = 'GZhY'
__version__ = 1.0


class Html2Image:
    def __init__(self, url, jscode=None):
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1200, 900)
        self.browser.get(url)
        self.jscode = jscode
        self.image = None

    def get_image(self):
        if self.jscode is not None and isinstance(self.jscode, JSInjection.JSCode) and self.jscode.get_jscode != "":
            # print(self.jsCode.getJSCode())
            self.browser.execute_script(self.jscode.get_jscode())
            for i in range(30):
                # print(self.browser.title)
                if self.jscode.finished_sign in self.browser.title:
                    break
                time.sleep(10)

        self.image = self.browser.get_screenshot_as_png()
        # self.browser.close()
        return self.image

    def get_element_image(self, css_selector):
        if self.image is None:
            self.get_image()
        element = self.browser.find_element_by_css_selector(css_selector)
        left, top = element.location['x'], element.location['y']
        right = left + element.size['width']
        bottom = top + element.size['height']
        im = Image.open(io.BytesIO(self.image))
        im = im.crop((left, top, right, bottom))
        # im.show()
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def save_image(self, image=None, filename="result.png"):
        if image is None:
            if self.image is None:
                image = self.get_image()
            else:
                image = self.image
        try:
            with open(filename, 'wb') as f:
                f.write(image)
        except IOError:
            return False
        finally:
            del image
        return True

    def __del__(self):
        self.browser.close()


if __name__ == '__main__':
    h2i = Html2Image("https://www.baidu.com/", JSInjection.Scroll2Bottom())
    h2i.save_image()
    h2i.save_image(h2i.get_element_image("#head > div > div.s_form > div"), "element.png")
