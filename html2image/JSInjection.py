#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is a JavaScript injection model."""
from abc import abstractmethod, ABCMeta

__author__ = 'GZhY'
__version__ = 1.0


class JSCode:
    __metaclass__ = ABCMeta

    finishedSign = "Hi, I completed the JS injection!"
    # 请在js代码表示执行完毕的位置加入此代码,外部函数会根据网页title中是否包含`finishedSign`来判断js代码是否执行完毕
    # js函数运行是异步的方式, 若js代码里有函数执行,直接把`finishedCode`加到最后是行不通的
    # 虽然有方法可以把函数改成同步方式,但没想到通式的方法(js盲),只能做这样处理了.
    finishedCode = "document.title += '" + finishedSign + "';"

    @abstractmethod
    def getJSCode(self):
        return ""


class Scroll2Bottom(JSCode):
    def getJSCode(self):
        return """(function () {
            var y = 0;
            var step = 100;
            var height = document.body.scrollHeight;
            function f() {
                //if (y < document.body.scrollHeight) {//这种情况下, 若html下拉会触发加载更多,会陷入循环内,直到加载完所有数据或函数运行时间超时
                if (y < height) { //这种情况下, 还是会触发加载更多, 但不会陷入循环中, 得到的图片可以进行裁剪, 或者根据屏幕分辨率事先算好触发加载更多的边界条件
                    y += step;
                    //window.document.body.scrollTop = y;
                    window.scrollTo(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scrollTo(0, 0);""" + self.finishedCode + """
                }
            }
            setTimeout(f, 1000);
        })();"""
