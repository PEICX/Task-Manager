#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-07 22:28:26
# @Author  : Law Paul (peicx@outlook.com)
# @Link    : http://github.com/peicx
# @Version : $Id$


from PyQt5 import QtWidgets
import sys
from UI_OS import Ui_MainWindow
import psutil
import os
import signal
import subprocess


def change(str):
    if len(str) < 14:
        return str.ljust(16)
    else:
        str = str[:13] + "..."
        return str


# 按照百分比格式化小数
def percent(num):
    str1 = str(round(num, 4)) + "%"
    # 内存占用比百分数长度小于7的，都加一个空格，方便对齐
    return str1.zfill(5)


def proc_stat(procid):
    # 获取系统全部进程
    proc = psutil.Process(procid)
    proc_info = []
    # 获取进程名
    proc_info.append(change(proc.name()))
    # 获取进程CPU占用率，并格式化对齐
    proc_info.append(percent(proc.cpu_percent()) + "    ")
    # 内存占用率
    proc_info.append(percent(proc.memory_percent()) + "    ")
    # 进程创建时间
    proc_info.append(str(proc.create_time()) + "    ")
    # 进程PID号
    proc_info.append(str(procid))
    return proc_info


def get_info():
    pro_list = psutil.pids()
    res = []
    for i in pro_list:
        try:
            res.append(' '.join(proc_stat(i)))
        except:
            return " "
    return res


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.listWidget.addItems(get_info())
        self.pushButton.clicked.connect(self.delete)
        self.actionend_task.triggered.connect(self.delete)
        self.pushButton_2.clicked.connect(self.refresh)
        self.actionflesh.triggered.connect(self.refresh)
        self.actionexit.triggered.connect(quit)
        self.actionopen_new_task.triggered.connect(self.create_pro)

    def delete(self):
        pid = str(self.listWidget.currentItem().text()).split()[-1]
        if os.name == 'nt':
            # win下终止进程
            os.popen('taskkill.exe /pid:' + str(pid))
        elif os.name == 'posix':
            # linux 下终止进程
            os.kill(pid, signal.SIGKILL)

    def refresh(self):
        self.listWidget.clear()
        self.listWidget.addItems(get_info())

    def create_pro(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, '进程创建', 'Input process')
        if ok:
            subprocess.Popen('%s' % text, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    TaskManager = QtWidgets.QApplication(sys.argv)
    windows = MyMainWindow()
    windows.show()
    sys.exit(TaskManager.exec_())
