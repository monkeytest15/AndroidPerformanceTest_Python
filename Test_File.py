# -*- coding: utf-8 -*-

import os, re,sys
import subprocess
import time, os, sched,shlex,threading
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF



# execute command, and return the output
def execCmd(cmd):
	r = os.popen(cmd)
	text = r.read()
	r.close()
	return text


def readShellBack():
	popen = subprocess.Popen(['adb', 'logcat'], stdout = subprocess.PIPE)
	while True:
		print popen.stdout.readline()

def catchException():
	try:
		readShellBack()
	except KeyboardInterrupt:
		print execCmd('adb devices')

def getAppPID(packagename):
	appPID_list = []
	args = shlex.split('adb shell top')
	popen = subprocess.Popen(args,stdout = subprocess.PIPE)
	Status = True
	try:
		while Status:
			logcat = popen.stdout.readline()
			if packagename in logcat:
				Status=False
				for pid in logcat.split(' '):
					if pid.isalnum():
						print pid
						return pid
	except KeyboardInterrupt:
		return pid

def getGCfile():
	os.system("adb kill-server")
	os.system("adb devices")
	print '日志正在记录中'
	try:
		os.system("adb logcat -v time -v threadtime *:D | grep GC>GCFile.txt")
	except KeyboardInterrupt:
		print 'GC logcat is over'

def MakePDF(times,list,reportname,pdfname):
	drawing = Drawing(500,300)
	lp = LinePlot()
	lp.x = 50
	lp.y = 50
	lp.height = 125
	lp.width = 300
	lp.data = [zip(times, list)]
	lp.lines[0].strokeColor = colors.blue
	lp.lines[1].strokeColor = colors.red
	lp.lines[2].strokeColor = colors.green

	drawing.add(lp)
	drawing.add(String(350,150, reportname,fontSize=14,fillColor=colors.red))

	renderPDF.drawToFile(drawing,pdfname,reportname)


def analysisGCFile(AppPID):
	GC_Freed =0
	GC_Freed_All =0
	GC_per =0
	GC_per_all =0
	GC_time = 0
	GC_time_all =0
	GC_Freed_list = []
	GC_per_list = []
	GC_time_list = []
	GC_count_list = []
	GC_count =0
	for data in open('GCFile.txt'):
		for i in data.split(' '):
			if  AppPID == i and 'freed' in data:
				GC_Freed = int(filter(str.isdigit,data.split(' ')[(data.split(' ').index('freed'))+1]))
				GC_Freed_list.append(GC_Freed)
				GC_Freed_All = GC_Freed_All+GC_Freed
				GC_per = int(filter(str.isdigit,data.split(' ')[(data.split(' ').index('freed'))+2]))
				GC_per_list.append(GC_per)
				GC_per_all = GC_per_all+GC_per
				number1 = data.split(' ')[(data.split(' ').index('freed'))+8]
				if '+' in number1:
					GC_time = int(filter(str.isdigit,number1.split('+')[0]))+int(filter(str.isdigit,number1.split('+')[1]))
					GC_time_all=GC_time_all+GC_time
					GC_time_list.append(GC_time)
				else:
					GC_time = int(number1[:-4])
					GC_time_all=GC_time_all+GC_time
					GC_time_list.append(GC_time)
				print GC_time
				GC_count = GC_count+1
				GC_count_list.append(GC_count)
	average_GC_Freed = '%.2f'%float(GC_Freed_All/GC_count)
	average_GC_per = '%.2f'%float(GC_per_all/GC_count)
	average_GC_time = '%.2f'%float(GC_time_all/GC_count)
	print GC_Freed_list,average_GC_Freed,GC_count_list,GC_per_list,average_GC_per,GC_time_list,average_GC_time
	return GC_Freed_list,average_GC_Freed,GC_count_list,GC_per_list,average_GC_per,GC_time_list,average_GC_time

def analysisTrafficFile(packagename):
	TrafficDataList=[]
	TrafficDataList2=[]
	TrafficCount =0
	TrafficCountList =[]
	for data in open('NetWorkFile.txt'):
		if packagename in data:
			TrafficDataList.append(int(data.split(' ')[len(data.split(' '))-1]))
			TrafficCount =TrafficCount+1
			TrafficCountList.append(TrafficCount)
	for i in TrafficDataList:
		TrafficDataList2.append(float(i-TrafficDataList[0])/1024)
	return TrafficCountList,TrafficDataList2


def WriteLog(waittime):
	try:
		subprocess.Popen("adb logcat -v time -v threadtime *:D | grep GC>GCFile.txt",shell=True)
		subprocess.Popen("adb logcat -v time *:E | grep Python2Android>NetWorkFile.txt",shell=True)
		print '日志正在记录中。。。请稍后'
		time.sleep(float(waittime)*3600)
	except KeyboardInterrupt:
		print '报告正在生成'
		os.system('adb kill-server')


schedule = sched.scheduler(time.time, time.sleep) 
    
def perform_command(cmd, inc): 
    os.system(cmd) 
        
def timming_exe(cmd, inc = 60): 
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
    schedule.enter(inc, 0, perform_command, (cmd, inc)) 
    # 持续运行，直到计划时间队列变成空为止 
    schedule.run() 
        
#timming_exe("echo %time%", 10)

if __name__=="__main__":
	app_pid = getAppPID(sys.argv[1])
	WriteLog(sys.argv[2])
	TrafficCountList,TrafficDataList = analysisTrafficFile(sys.argv[1])
	print TrafficCountList,TrafficDataList,'xxxx'
	MakePDF(TrafficCountList,TrafficDataList,'average Traffic:'+'kb',"流量消耗.pdf")
	GC_Freed_list,average_GC_Freed,GC_count_list,GC_per_list,average_GC_per,GC_time_list,average_GC_time= analysisGCFile(app_pid)
	MakePDF(GC_count_list,GC_Freed_list,'average GC Freed:'+str(average_GC_Freed)+'kb',"GC_Freed报告.pdf")
	MakePDF(GC_count_list,GC_per_list,'average GC per:'+str(average_GC_per)+'%',"GC_百分比报告.pdf")
	MakePDF(GC_count_list,GC_per_list,'average GC time:'+str(average_GC_time)+'ms',"GC_时间消耗.pdf")

