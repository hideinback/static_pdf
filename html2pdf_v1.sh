#!/bin/bash

# description: convert html to pdf
# author: Zhang Fangxian, zhangfx@genomics.cn
# created date: 20100504
# modified date: 20100510, 20100507, 20120828

if [ $# -lt 2 ]; then
	echo "usage: $0 html [head.html] pdf" >&2
	exit 1
fi

path=`dirname $0`

# install font
if [ ! -f ~/.fonts/wqy-microhei.ttc ]; then
	wqy=$path/`ls -1 $path | grep wqy-microhei | tail -n 1`

	echo installing wqy font...
	if [ ! -d ~/.fonts ]; then
		mkdir ~/.fonts
	fi
	tar zxf $wqy
	cp wqy-microhei/*.ttc  ~/.fonts
	rm -rf wqy-microhei
fi
if [ $3 ];then
	# convert html to pdf
	/root/Software/miniconda3/envs/ora/bin/wkhtmltopdf --quiet --disable-internal-links --disable-external-links --print-media-type -O Landscape --footer-center '[page]/[toPage]'  --header-line --header-html $2 --header-spacing 5 -s A4 -T 20mm -R 5mm -B 5mm -L 5mm $1 $3
else
	#$path/wkhtmltopdf-amd64 --quiet --disable-internal-links --disable-external-links --print-media-type -O Landscape --footer-center '[page]/[toPage]'  -s A4 -T 5mm -R 5mm -B 5mm -L 5mm $1 $2
	#echo "$path/wkhtmltopdf-amd64 --quiet -s A4 -T 10mm -R 8mm -B 10mm -L 8mm --outline --toc --toc-header-text 目录 --cover $path/cover.html $1 $2"
	/root/Software/miniconda3/envs/ora/bin/wkhtmltopdf --quiet -s A4 -T 10mm -R 8mm -B 10mm -L 8mm --outline toc --toc-header-text Catalogue cover $path/cover.html $1 $2
fi
exit 0
