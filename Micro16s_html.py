#!/root/Software/miniconda3/bin/python3 -w
#-*- coding:utf8 -*-

__author__= 'xiazhanfeng' 

import os
import re
import sys
from collections import defaultdict
import argparse
import configparser
from htmlstaticpdf import Myhtml,Index
import pdfkit

__author__ = "xiazhanfeng"
__version__ = '$Revision: 1 $'
__date__ = '$20 May 2020 $'



def html_pipeline(configfile, out, limit=""):
	
	config = Myhtml.read_config(configfile)
	config_keylist = list(config.keys())
	myindex = Index(config['main']['title'], limit)
	for i in range(1,len(config_keylist)-1):
		myindex.htmlize(dict(config[str(i)]))
	myindex.myhtml.html_outprint(out)


def html2pdf(html, pdf, software="/root/Software/miniconda3/envs/ora/bin/wkhtmltopdf",cover = "/root/16s/Modules/static_pdf/src/cover.html"):
	options = {'page-size': 'A4', 'margin-top': '0.75in', 'margin-right': '0.75in', 'margin-bottom': '0.75in', 'margin-left': '0.75in', 'encoding': 'UTF-8', 'outline': None}
	config  = pdfkit.configuration(wkhtmltopdf=software)
	try:
		pdfkit.from_file(html, pdf, cover="/root/16s/Modules/static_pdf/cover.html", options=options, configuration=config, toc={'toc-header-text':'目录'}, cover_first=True)
	except Exception as e:
		print(e)
	

if __name__  == '__main__':
	parser = argparse.ArgumentParser(description='Reading config and producing my html format module by pyh')
	parser.add_argument('--config','-c', required=True, help='config file for html')
	parser.add_argument('--out','-o', required=True, help='out html filename')
	parser.add_argument('--limit','-l', required=False, help='limit for table row number', default="")
	args = parser.parse_args()
	config = args.config
	out = args.out
	limit = args.limit
	html_pipeline(config, out, limit)
	prefix, suffix = os.path.splitext(out)
	html2pdf(out, prefix + ".pdf")
