# -*- coding: utf-8 -*-

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
	return time_array[0]+'_'+time_array[1]+"_"+time_array[2]

def run_monkey(param,package_name,count,waittime):
	try:
		if param == 'Normal':
			subprocess.Popen("adb shell monkey -p %s --pct-motion 20 --pct-trackball 0 --pct-touch 40 --pct-nav 10 --ignore-crashes --ignore-timeouts --throttle 300 -v -v -v %d >MonkeyTest_Report_%s.txt"%(package_name,count,now_time()),shell=True)
		if param == 'alltouch':
			subprocess.Popen("adb shell monkey -p %s --pct-touch 100 --ignore-crashes --ignore-timeouts --throttle 300 -v -v -v %d >MonkeyTest_Report_%s.txt"%(package_name,count,now_time()),shell=True)
		if param == 'other':
			subprocess.Popen("adb shell monkey -p %s --pct-majornav 30 --pct-syskeys 30 --pct-anyevent 30 --ignore-crashes --ignore-timeouts --throttle 300 -v -v -v %d >MonkeyTest_Report_%s.txt"%(package_name,count,now_time()),shell=True)
		print 'Monkey日志正在记录中。。。请稍后'
		time.sleep(float(waittime)*1)
	except KeyboardInterrupt:
		print '报告正在生成'
		os.system('adb kill-server')
		os.system('adb devices')


if __name__ == '__main__':
	run_monkey(sys.argv[1],sys.argv[2],argv[3],argv[4])