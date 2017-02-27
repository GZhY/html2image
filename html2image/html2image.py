#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This is a XXX script.
What is the function of this script? """

__author__ = 'GZhY'
__version__ = 1.0

from selenium import webdriver
import time
import JSInjection


def getImage(url, jsCode=None, saveImageName="result.png"):
    browser = webdriver.PhantomJS()
    browser.set_window_size(1200, 900)
    browser.get(url)
    if jsCode is not None and isinstance(jsCode, JSInjection.JSCode) and jsCode.getJSCode != "":
        print(jsCode.getJSCode())
        browser.execute_script(jsCode.getJSCode())
        for i in range(30):
            print(browser.title)
            if jsCode.finishedSign in browser.title:
                break
            time.sleep(10)

    browser.save_screenshot(saveImageName)
    browser.close()


def getElementImage():
    pass


if __name__ == '__main__':
    getImage("http://www.baidu.com", JSInjection.Scroll2Bottom())
