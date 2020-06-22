## Micro 16S 静态报告生成文档

一. 模块基于python3 pyh库生成html格式文本, 文本内容依据自行配置的config文件顺序进行转换[*目前标题只能深入至第二层级*].

```shell
usage: htmlstaticpdf.py [-h] --config CONFIG --out OUT --limit LIMIT

Reading config and producing my html format module by pyh

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        config file for html
  --out OUT, -o OUT     out html filename
  --limit LIMIT, -l LIMIT
                        limit table row number; restrict the rows of table which exhibit in PDF
```

二. 配置

```shell
[main]
#根据index去识别整体html排版
title=Micro16s static brief report

[1]
subtitle = 1 项目信息
prolog =
topic = 本项目的基本信息见下表:
caption = 表1  项目信息
tablepath = src/project.info
type = table
conclusion =

[2]
subtitle = 2 实验流程
prolog =
topic  = 取质量合格的基因组DNA样品30ng及对应的融合引物配置PCR反应体系...
caption = 图1  实验流程.
pngpath = src/实验图.png
type = png
conclusion =

[3]
subtitle = 3 信息分析流程
caption = 图2  信息分析流程.
prolog =
topic = 下机数据过滤，剩余...
pngpath = src/流程图.png
type = png
conclusion =
```

```shell
[main] title为html打开时的名称(无具体意义)
[1],[2],[3],[4]...根据该顺序一次进行transform
subtitle = [该模块标题]
prolog = [次级标题]
topic = [正文]
caption = [表或者图的上标下标, 目前默认表为上标,图为下标]
tablepath = [表格绝对路径, 也可为其他参数pngpath]
type = table[table or png]
conclusion = [表或者图的后缀说明]
```

三. 应用

```shell
usage: Micro16s_html.py [-h] --config CONFIG --out OUT [--limit LIMIT]

Reading config and producing my html format module by pyh

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        config file for html
  --out OUT, -o OUT     out html filename
  --limit LIMIT, -l LIMIT
                        limit for table row number
```

Micro16s_html.py 是对htmlstaticpdf.py进行了简单包装, 一般使用为该脚本, 参数与htmlstaticpdf.py保持一致, 其中添加了wkhtmltopdf对html进行转换的函数, 所以最后也会得到html和pdf的2个文件；out由于为html文件,所以尽量使用html的后缀。
具体示例可参考16s.html和16.pdf结果文件, 示例配置为static_pdf-config.txt文件

四. 流程

```shell
usage: Static_staic_report.py [-h] --indir INDIR --outdir OUTDIR
                              [--basedir BASEDIR] [--config CONFIG]
Produce Staic PDF Config

optional arguments:

	-h, --help            show this help message and exit
	--indir INDIR, -i INDIR
				input Report dirpath
	--outdir OUTDIR, -o OUTDIR
				out dir path
	--basedir BASEDIR, -b BASEDIR
				base src dir(default script root dir)
	--config CONFIG, -c CONFIG
				config path(default outdir report.config)
```

