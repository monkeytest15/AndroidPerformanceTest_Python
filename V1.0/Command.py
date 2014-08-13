# -*- coding: utf-8 -*-

'''
by monkey
'''


import os, re,sys
import subprocess
import time, os, sched,shlex,threading
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

def now_time():
	localtime = time.asctime( time.localtime(time.time()) )
	time_array = localtime.split(" ")[3].split(":")
	print time_array
	return time_array[0]+'_'+time_array[1]+"_"+time_array[2]

def WriteLog(waittime,package_name):
	try:
		subprocess.Popen("adb shell top >App_cpu_%s.txt"%now_time(),shell=True)
		subprocess.Popen("adb logcat | grep ActivityManager >Start_Time_%s.txt"%now_time(),shell=True)
		subprocess.Popen("adb logcat | grep GC >GC_Data_%s.txt"%now_time(),shell=True)
		subprocess.Popen("adb shell dumpsys meminfo %s >Meminfo_%s.txt"%(package_name,now_time()),shell=True)
		subprocess.Popen("adb logcat -v time *:E | grep com.alipay.m.portaltrafficeTest >NetWorkFile_%s.txt"%now_time(),shell=True)
		subprocess.Popen("adb logcat -v time *:E | grep battery >batteryFile_%s.txt"%now_time(),shell=True)
		print '日志正在记录中。。。请稍后'
		print '各个界面启动时间正在记录。。。请稍后'
		print '应用每个功能cpu占用率正在记录。。。请稍后'
		print '应用GC回收和使用时间正在记录。。。请稍后'
		print '应用内存正在记录。。。请稍后'
		print '应用网络数据正在记录。。。请稍后'
		print '应用电量数据正在记录。。。请稍后'
		time.sleep(float(waittime)*1)
	except KeyboardInterrupt:
		print '报告正在生成'
		os.system('adb kill-server')

if __name__ == '__main__':
	WriteLog(sys.argv[1],sys.argv[2])