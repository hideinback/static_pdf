#!/usr/bin/python -w
#-*- coding:utf8 -*-

__author__= 'xiazhanfeng' 

import os
import re
import sys
from collections import defaultdict
import argparse
import logging
import configparser
from pyh import *
from PIL import Image

__author__ = "xiazhanfeng"
__version__ = '$Revision: 1 $'
__date__ = '$Fri, 15 May 2020 $'


class Myhtml():
	'''按照文章格式建立对象创建上手的html文本'''
	
	def __init__(self, title, limit = ""):
		#self.out = out
		self.html_title(title)
		self.limit = limit 
	
	
	def html_outprint(self, out):
		self.page.printOut(out)


	def html_png(self, pngpath, title, pos="center"):
		pngdiv = self.page <<div(style = "text-align: %s" % pos)
		width_num, height_num = self.suit_a4(pngpath)
		#pngdiv << p(title, style = "text-align: %s" % pos)
		pngdiv << img(src = pngpath, width=width_num, height=height_num)
		pngdiv << p(title, style = "text-align: %s" % pos)


	@staticmethod
	def suit_a4(pngpath, axis = 'width'):
		a4w, a4h = 1000, 1800
		image = Image.open(pngpath)
		w, h = image.size
		#print(image.size)
		if axis == "width":
			return a4w, round(h/(w/(a4w*0.85)),2)
		elif axis == "height":
			return round(w/(h/(a4h*0.85)),2), a4h
		


	def html_table(self, tablepath, title, limit = ""):
		'''需有表头'''
		
		table_hash = self.read_table(tablepath, limit)
		#属性
		self.page << br()
		tablediv = self.page <<div()
		#加表标题
		tablediv << p(title, style = "text-align: left")
		mytable = tablediv << table(border="1", cellpadding ="3", cellspacing = "0")
		#表头颜色
		tr1 = mytable <<tr(bgcolor = "#48a6fb", align="all")
		#列名
		header_generator = ("th(\"%s\")" % str(ele) for ele in table_hash['1'])
		header_string = ""
		for ele in header_generator:
			if header_string:
				header_string = header_string + " + " + ele
			else:
				header_string = ele
		tr1<<eval(header_string)
		#填充表格
		for i in range(2,len(table_hash.keys())):
			tr2 = mytable <<tr()
			for j in range(len(table_hash[str(i)])):
				tr2<<td(str(table_hash[str(i)][j]))
		#加表标题
		#tablediv << p(title, style = "text-align: left")


	
	def html_slide(self, pnglist):
		print("Not Achieve slide png")
		pass
	

	def html_div(self, desc, level=2, pos="left"):
		'''标题文字, 几级标题, 标题位置'''
		if not desc:
			return ""
		if level:
			if level<=4:
				voidline = (4-level)*"br() +"
				voidline = re.sub(r'\+$', "", voidline)
				self.page << eval(voidline)
			flag = "h" + str(level)
			mydiv = self.page <<div(style="text-align:" + pos)<< eval(flag)(desc)


	def html_title(self, title):
		'''header内部标签,网页打开html可看到,pdf则无法查看'''
		self.page = PyH(title)
		

	def html_divpara(self, desc, pos="left", bold=0):
		'''正文描述, 正文位置, 是否加粗'''
		#desc = eval(desc)
		#print(r''+desc)
		descs = re.split('\\\\n', desc)
		#print(descs)
		desc_string = '+'.join("p(\"%s\", style = \"text-align:%s\")"% (i, pos) for i in descs)
		dpdiv = self.page <<div(style="text-align:" + pos)
		if bold:
			dpdiv << b() + eval(desc_string) 
		else:
			dpdiv << eval(desc_string)


	@staticmethod
	def read_table(tablename, limit = ""):
		'''默认第一行为表头'''
		table_hash = defaultdict(list)
		te = open(tablename, 'r')
		index = 0
		for teline in te:
			index += 1
			if limit:
				if index > limit:
					return table_hash
			teline = teline.strip()
			telines = re.split('\s+', teline)
			table_hash[str(index)] = telines
		return table_hash

	
	@staticmethod
	def read_config(configfile):
		config = configparser.ConfigParser()
		config.read(configfile)
		return config


class Index():

	'''解析config里面的每种type[png, text, table, main等类型]'''
	def __init__(self, title, limit=""):
		self.myhtml = Myhtml(title, limit)
		#self.htmlize()
		

	def htmlize(self, infodict):
		if infodict['type'] == 'png':
			self.pnglize(infodict)
		elif infodict['type'] == 'table':
			self.tablelize(infodict)
		elif infodict['type'] == 'paragraph':
			self.paralize(infodict)
		elif infodict['type'] == 'slide':
			self.slidelize(infodict)


	def baseload(self, infodict):
		#标题
		basediv = self.myhtml.html_div(infodict['subtitle'], 2)
		self.myhtml.html_div(infodict['prolog'], 3)
		self.myhtml.html_divpara(infodict['topic'])
		#self.myhtml.html_divpara(infodict['caption'])
		return basediv


	def mainlize(self, infodict):
		'''目前只有title'''
		self.myhtml.html_title(infodict['title'])
		
	
	def slidelize(self, infodict):
		self.baseload(infodict)
		self.myhtml.html_slide(infodict['pnglist'])
		self.myhtml.html_divpara(infodict['conclusion'])


	def pnglize(self, infodict):
		#标题
		self.baseload(infodict)
		self.myhtml.html_png(infodict['pngpath'], infodict['caption'])
		self.myhtml.html_divpara(infodict['conclusion'], 'left')
		#self.myhtml.html_png(infodict['pngpath'], infodict['caption'])


	def tablelize(self, infodict):
		self.baseload(infodict)
		self.myhtml.html_table(infodict['tablepath'], infodict['caption'])
		self.myhtml.html_divpara(infodict['conclusion'], 'left')
		#self.myhtml.html_table(infodict['tablepath'], infodict['caption'])
	

	def paralize(self, infodict):
		tablediv = self.baseload(infodict)
		self.myhtml.html_divpara(infodict['conclusion'], 'left')


if __name__  == '__main__':
	parser = argparse.ArgumentParser(description='Reading config and producing my html format module by pyh')
	parser.add_argument('--config','-c', required=True, help='config file for html')
	parser.add_argument('--out','-o', required=True, help='out html filename')
	parser.add_argument('--limit','-l', required=True, help='limit table row number', default="")
	args = parser.parse_args()
	config = args.config
	out = args.out
	limit = args.limit
	#Myhtml(config, out)	
