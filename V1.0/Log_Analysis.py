# -*- coding: utf-8 -*-

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



def read_log(log_path):
	LogList = []
	f = open(log_path)
	s = f.readlines()
	f.close()
	for line in s:
		LogList.append(line)
	return LogList

def cpu_analysis():
	_data_list =[]
	_cpudata_list = []
	cpu_list = read_log(cpu_path)
	for i in xrange(len(cpu_list)):
		_data_list.append(cpu_list[i].split(" "))
	for i in xrange(len(_data_list)):
		for j in xrange(len(_data_list[i])):
			_noblank_list = [elem for elem in _data_list[i] if elem != ""]
			for k in xrange(len(_noblank_list)):
				if package_name in _noblank_list[k]:
					_cpudata_list.append(_noblank_list[2])
	print _cpudata_list


def Memory_Vss_analysis():
	_data_list =[]
	_Vssdata_list = []
	cpu_list = read_log(cpu_path)
	for i in xrange(len(cpu_list)):
		_data_list.append(cpu_list[i].split(" "))
	for i in xrange(len(_data_list)):
		for j in xrange(len(_data_list[i])):
			_noblank_list = [elem for elem in _data_list[i] if elem != ""]
			for k in xrange(len(_noblank_list)):
				if package_name in _noblank_list[k]:
					_Vssdata_list.append(_noblank_list[5])
	print _Vssdata_list	

def Memory_Vss_analysis():
	_data_list =[]
	_Vssdata_list = []
	memory_list = read_log(cpu_path)
	for i in xrange(len(memory_list)):
		_data_list.append(memory_list[i].split(" "))
	for i in xrange(len(_data_list)):
		for j in xrange(len(_data_list[i])):
			_noblank_list = [elem for elem in _data_list[i] if elem != ""]
			for k in xrange(len(_noblank_list)):
				if package_name in _noblank_list[k]:
					_Vssdata_list.append(_noblank_list[5])
	print _Vssdata_list

def Memory_Rss_analysis():
	_data_list =[]
	_Rssdata_list = []
	memory_list = read_log(cpu_path)
	for i in xrange(len(memory_list)):
		_data_list.append(memory_list[i].split(" "))
	for i in xrange(len(_data_list)):
		for j in xrange(len(_data_list[i])):
			_noblank_list = [elem for elem in _data_list[i] if elem != ""]
			for k in xrange(len(_noblank_list)):
				if package_name in _noblank_list[k]:
					_Rssdata_list.append(_noblank_list[5])
	print _Rssdata_list

def Gc_analysis():
	_gc_free_list =[]
	_gc_used_per = []
	_gc_total_time = []
	gc_list = read_log(gc_path)
	for i in xrange(len(gc_list)):
		if 'GC_CONCURRENT' in gc_list[i]:
			freed_index =  gc_list[i].split(' ')[5]
			_gc_free_list.append(gc_list[i].split(' ')[3])
			_gc_used_per.append(gc_list[i].split(' ')[4])
			_gc_total_time.append(gc_list[i].split(' ')[10][-4:])
#	print _gc_total_time







if __name__=="__main__":
	cpu_analysis()