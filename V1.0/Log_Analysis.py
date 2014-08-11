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

cpu_path = "/Users/monkey/Pictures/performance_test_script/App_cpu_13_36_54.txt"
gc_path = '/Users/monkey/Pictures/performance_test_script/GC_file.txt'
package_name = 'com.alipay.m.portal'
flow_path ='/Users/monkey/Pictures/performance_test_script/NetWorkFile_13_36_54.txt'



class Read_file:
	def __init__(self):
		self.LogList = []

	def read_log(self,log_path):
		f = open(log_path)
		s = f.readlines()
		f.close()
		for line in s:
			self.LogList.append(line)
		return self.LogList

def cpu_analysis():
	_data_list =[]
	_cpudata_list = []
	cpu_total = 0
	cpu_file = Read_file()
	cpu_list = cpu_file.read_log(cpu_path)
	try:
		for i in xrange(len(cpu_list)):
			_data_list.append(cpu_list[i].split(" "))
		for i in xrange(len(_data_list)):
			for j in xrange(len(_data_list[i])):
				_noblank_list = [elem for elem in _data_list[i] if elem != ""]
				for k in xrange(len(_noblank_list)):
					if package_name in _noblank_list[k]:
						_cpudata_list.append(_noblank_list[2])
						cpu_total = cpu_total+int(_noblank_list[2][:-1])
		avg_cpu = cpu_total/len(_cpudata_list)
	except IndexError:
		print "日志文件不完整"
	return _cpudata_list,avg_cpu

def Memory_Vss_analysis():
	_data_list =[]
	_Vssdata_list = []
	Memory_total = 0
	Memory_file = Read_file()
	memory_list = Memory_file.read_log(cpu_path)
	try:
		for i in xrange(len(memory_list)):
			_data_list.append(memory_list[i].split(" "))
		for i in xrange(len(_data_list)):
			for j in xrange(len(_data_list[i])):
				_noblank_list = [elem for elem in _data_list[i] if elem != ""]
				for k in xrange(len(_noblank_list)):
					if package_name in _noblank_list[k]:
						_Vssdata_list.append(_noblank_list[5])
						Memory_total = Memory_total+int(_noblank_list[5][:-1])
		avg_Vss = Memory_total/len(_Vssdata_list)
	except IndexError:
		print "日志文件不完整"
	return _Vssdata_list,avg_Vss

def Memory_Rss_analysis():
	_data_list =[]
	_Rssdata_list = []
	Memory_total = 0
	Memory_file = Read_file()
	memory_list = Memory_file.read_log(cpu_path)
	try:
		for i in xrange(len(memory_list)):
			_data_list.append(memory_list[i].split(" "))
		for i in xrange(len(_data_list)):
			for j in xrange(len(_data_list[i])):
				_noblank_list = [elem for elem in _data_list[i] if elem != ""]
				for k in xrange(len(_noblank_list)):
					if package_name in _noblank_list[k]:
						_Rssdata_list.append(_noblank_list[6])
						Memory_total = Memory_total+int(_noblank_list[5][:-1])
		avg_Rss = Memory_total/len(_Rssdata_list)
	except IndexError:
		print "日志文件不完整"
	return _Rssdata_list,avg_Rss

def Gc_analysis():
	_gc_free_list =[]
	_gc_used_per = []
	_gc_total_time = []
	_gc_free_total = 0
	_gc_used_total = 0
	_gc_time_total =0
	gc_file = Read_file()
	gc_list = gc_file.read_log(gc_path)
	try:
		for i in xrange(len(gc_list)):
			if 'GC_CONCURRENT' in gc_list[i]:
				freed_index =  gc_list[i].split(' ').index('freed')
				if gc_list[i].split(' ')[freed_index+1][:-2].isdigit() and gc_list[i].split(' ')[freed_index+2][:-1].isdigit() and gc_list[i].split(' ')[len(gc_list[i].split(' '))-1][:-4].isdigit():
					_gc_free_list.append(gc_list[i].split(' ')[freed_index+1])
					_gc_used_per.append(gc_list[i].split(' ')[freed_index+2])
					_gc_total_time.append(gc_list[i].split(' ')[len(gc_list[i].split(' '))-1][:-4])
					_gc_free_total = _gc_free_total+int(gc_list[i].split(' ')[freed_index+1][:-2])
					_gc_used_total = _gc_used_total+int(gc_list[i].split(' ')[freed_index+2][:-1])
					_gc_time_total = _gc_time_total + int(gc_list[i].split(' ')[len(gc_list[i].split(' '))-1][:-4])
		avg_gc_free = _gc_free_total/len(_gc_free_list)
		avg_gc_used = _gc_used_total/len(_gc_used_per)
		avg_gc_time = _gc_time_total/len(_gc_total_time)
	except IndexError:
		print "日志文件不完整"
	return _gc_free_list,_gc_used_per,_gc_total_time,avg_gc_free,avg_gc_used,avg_gc_time


def flow_analysis():
	_flow_list = []
	flow_file = Read_file()
	flow_list = flow_file.read_log(flow_path)
	flow_total =0
	try:
		for i in xrange(len(flow_list)):
			_flow_list.append(flow_list[i].split(' ')[-1:][0][:-4])
			flow_total = flow_total+int(flow_list[i].split(' ')[-1:][0][:-4])
		avg_flow = flow_total/len(_flow_list)
	except IndexError:
		print "日志不完整"
	print _flow_list,avg_flow







if __name__=="__main__":
	flow_analysis()