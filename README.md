# douban2
# douban movie based on scrapy #

一个基于scrapy框架的豆瓣电影爬虫

测试环境windows， python3.5.4， miniconda 虚拟环境

运行方法

1. python runner.py

	使用scrapydo框架配置管理运行爬虫
2. scrapy crawl doubanmovie
3. 其他运行管理模块如scrapyd




**爬取豆瓣电影时，遇到几种封锁方法，服务器会将请求重定向到sec.douban.movie（200状态码 ->302状态码->403状态码，提示ip异常） 、https://www.douban.com/misc/sorry？（弹出验证码）、 返回javascript脚本（200状态码，无可用信息） 对于前两种封锁，统计错误次数，超过规定数额后关闭爬虫、换ip、开启爬虫 对于后面一种情况，写了一个下载中间件，检查https://movie.douban.com/subject/xxxxxx/类网址，内容过少时，返回scrapy Request实例**
