#!/root/Software/miniconda3/bin/python3
#-*- coding:utf8 -*-

__author__= 'xiazhanfeng'

import os
import re
import sys
from collections import defaultdict
import argparse
import configparser
import json
import yaml
import shutil
from Micro16s_html import html_pipeline, html2pdf


class configout():
	'''根据Report路径生成静态报告需要的config配置文件'''
	
	def __init__(self, indir, outdir, basedir, configfile):
		self.outdir = outdir 
		self.basedir = basedir
		self.configfile = configfile
		self.indir = indir
		self.samplenum = 0
		if not os.path.isdir(self.outdir):
			os.makedirs(self.outdir)
		if os.path.lexists(self.indir):
			if os.path.lexists(str(self.indir) + "/analysis_plan.yml"):
				self.load_yaml(str(self.indir) + "/analysis_plan.yml")
			else:
				print(str(self.indir + "/analysis_plan.yml") + " Non-Exists")
				sys.exit()
		else:
			print(str(self.indir) + " Non-Exists")
			sys.exit()
		
		self.config = configparser.ConfigParser()
		binpath = os.path.dirname(os.path.realpath(sys.argv[0]))
		if not basedir:
			self.basedir = binpath + "/src"
		if not configfile:
			self.configfile = binpath + "/static_pdf-config.txt"
		self.config.read(self.configfile)


	def proscript(self):
		projectfile = self.outdir + "/project.info" 
		self.header_move(self.basedir)
		self.project_static(projectfile)
		self.clean_static()
		self.joint_static()
		self.cluster_static()
		self.anno_static()
		self.barplot_static()
		rc = open(self.outdir + "/report.config", 'w')
		self.config.write(rc)
		rc.close()


	def load_yaml(self, jsonfile):
		'''读取report中yaml文件'''
		ye = open(jsonfile, 'r')
		self.jsondict= yaml.safe_load(ye)
		ye.close()


	def project_static(self, projectfile):
		#项目编号, 测序区域, Tag数据量(默认50000), 注释数据库, 样本数量
		project_info = {}
		pe = open(projectfile, 'w')
		pe.write("项目信息\t描述\n")
		if self.jsondict.get('projects'):
			pe.write("项目编号\t" + ','.join(str(i) for i in self.jsondict['projects']) + "\n")
		if self.jsondict.get('region'):
			pe.write("测序区域\t" + str(self.jsondict['region']) + "\n")
		if not self.jsondict.get('tagnumber'):
			self.jsondict['tagnumber'] = 50000
		pe.write("Tag数据量\t" + str(self.jsondict['tagnumber']) + "\n")
		if self.jsondict.get('database'):
			pe.write("注释数据库\t" + str(self.jsondict['database']) + "\n")
		pe.close()
		self.config.set("1", "tablepath", projectfile)

	
	def header_move(self, basedir):
		'''copy src至生成报告的目录'''
		#if not os.path.lexists(basedir):	
		if os.path.lexists(self.outdir + "/src"):
			if os.path.isdir(self.outdir + "/src"):
				shutil.rmtree(self.outdir + "/src")
			else:
				os.remove(self.outdir + "/src")
		#print(basedir + "\t" + self.outdir + "/src")
		shutil.copytree(basedir, self.outdir + "/src")

	
	def clean_static(self):
		if os.path.lexists(self.indir + "/otu/otu_stat/CleanData_stat.xls"):
			shutil.copy(self.indir + "/otu/otu_stat/CleanData_stat.xls", self.outdir + "/CleanData_stat.xls")
			self.config.set("4", "tablepath", self.outdir + "/CleanData_stat.xls")


	def joint_static(self):
		tagfile = self.indir + "/otu/otu_stat/Tag_stat.xls"
		if os.path.lexists(tagfile):
			te = open(tagfile, 'r')
			to = open(self.outdir + "/Tag_stat.xls", 'w')
			self.config.set("5", "tablepath", self.outdir + "/Tag_stat.xls")
			for teline in te:
				teline = teline.strip()
				telines = re.split('\s+', teline)
				if re.search(r'^\s*$', teline):
					continue
				if re.search(r'Summary of Sample\'s Reads and Tags', teline):
					te.close()
					to.close()
					return ""
				to.write('\t'.join(str(i) for i in telines[0:5]) + "\n")
				self.samplenum += 1
			self.config.set("1", "Samplenumber", str(self.samplenum - 1))


	def cluster_static(self):
		clusterfile = self.indir + "/otu/otu_stat/OTU_stat_detail.xls"
		if os.path.lexists(clusterfile):
			ce = open(clusterfile, 'r')
			co = open(self.outdir + "/OTU_stat_detail.xls", 'w')
			self.config.set("6", "tablepath", self.outdir + "/Tag_stat.xls")
			flag = 0
			for celine in ce:
				celine = celine.strip()
				if re.search(r'^\s*$', celine):
					continue
				if re.search(r'Sample detail:', celine):
					flag = 1
				if flag:
					co.write(celine + "\n")
			ce.close()
			co.close()


	def anno_static(self):
		pass	
	

	def barplot_static(self):
		barplot_png = self.indir + "/ann/barplot/all/Barplot.Sample.Genus.all.png"
		if os.path.lexists(barplot_png):
			shutil.copy(barplot_png, self.outdir)
			self.config.set("8", 'pngpath', barplot_png)
	



if __name__  == '__main__':
	parser = argparse.ArgumentParser(description='Produce Staic PDF Config')
	parser.add_argument('--indir','-i', required=True, help='input Report dirpath')
	parser.add_argument('--outdir','-o', required=True, help='out dir path')
	parser.add_argument('--basedir','-b', required=False, help='base src dir(default script root dir)', default="")
	parser.add_argument('--config','-c', required=False, help='config path(default outdir report.config)', default="")
	args = parser.parse_args()
	indir = args.indir
	outdir = args.outdir
	basedir = args.basedir
	config = args.config
	configs = configout(indir, outdir, basedir, config)
	configs.proscript()
	html_pipeline(configs.outdir + "/report.config", configs.outdir + "/report.html")
	html2pdf(configs.outdir + "/report.html", configs.outdir + "/report.pdf")
