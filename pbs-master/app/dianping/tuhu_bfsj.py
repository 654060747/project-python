# encoding='utf-8'
import time,os
from selenium import webdriver
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

def select_css(count,data,css,title):
	if count == 1:
		return data.select(css)
	if count == 2:
		return data.select(css)[0].getText().strip()
	if count == 3:
		return data.select(css)[0].get(title)


def data_(driver):
	time.sleep(1.5)
	html = driver.page_source 
	data = str(pq(html))  
	data = BeautifulSoup(data,"lxml")
	data.encoding = 'utf-8'
	return data

def find_result_data(driver,j,css_,data,by_lx,by_son):
	# 拿到项目名
	css = css_+"tr:nth-child("+str(j)+") > td:nth-child(1) > p"
	by_name = select_css(2,data,css,'')
	# print(by_name)
	# 拿到每个项目下的内容数
	string_buffer = ''
	css = css_+"tr:nth-child("+str(j)+") > td:nth-child(2) > div"
	div_list = select_css(1,data,css,'')
	for z in range(1,len(div_list)+1):
		# 点击内容列
		css = css_+"tr:nth-child("+str(j)+") > td:nth-child(2) > div:nth-child("+str(z)+")"
		driver.find_element_by_css_selector(css).click()
		data = data_(driver)
		time.sleep(2)
		# 得到产品列表
		css = "#changeProductList > div"
		div_list_ = select_css(1,data,css,'')
		print(len(div_list_))
		for m in range(2,len(div_list_)+1):
			
			css_ = "#changeProductList > div:nth-child("+str(m)+") >"
			# 拿到产品链接
			css = css_+"a.name"
			product_url = select_css(3,data,css,"href")
			print(product_url)
		# 	time.sleep(1)
	# 		# 拿到产品图片
	# 		css = css_+"a:nth-child(1) > img"
	# 		product_pic = select_css(3,data,css,'src')
	# 		# 拿到列表内容
	# 		css = css_+"a:nth-child(2) > span.productTitle"
	# 		product_content = select_css(2,data,css,'')
	# 		# 拿到规格
	# 		css = css_+"a:nth-child(2) > span.itemTag.qianscp"
	# 		product_spec = select_css(2,data,css,'')
	# 		print(product_spec)
	# 		if product_spec == None:
	# 			product_spec = " "
	# 		# 拿到列表价格
	# 		css = "div"
	# 		product_price = select_css(2,data,css,'')


	# 		string_buffer = string_buffer + product_url +","+ product_pic +","+ product_content +","+ product_spec + ","+ product_price + ";"

	# print(by_lx+","+by_son+","+by_name+","+string_buffer)


def by_lx_open(driver,data,baoyang_dict):
	# 拿到子项点开的详细条数
	css = "#productList > div"
	div_list = select_css(1,data,css,'')
	for i in range(1,len(div_list)+1):
		css = "#productList > div:nth-child("+str(i)+") > div > span.name"
		by_son = select_css(2,data,css,'')
		# print(by_son)
		# 字典查找对应保养类型
		for by_son_one in baoyang_dict:
			if by_son_one in by_son:
				by_lx = baoyang_dict[by_son_one]
		# 拿到每个子项下的项目数量
		css_ = "#productList > div:nth-child("+str(i)+") > table > tbody >"
		css = css_+"tr"
		tr_list = select_css(1,data,css,'')
		for j in range(1,len(tr_list)+1):
			# 取数据
			find_result_data(driver,j,css_,data,by_lx,by_son)
			

def by_list(data,driver,url_one):
	dl_list = data.select("#package_baoyang > dl")
	if len(dl_list) == 0:
		print("网页没有数据==="+url_one)
	baoyang_dict = {}
	for i in range(1,len(dl_list)+1):
		# 拿到保养类型
		css = "#package_baoyang > dl:nth-child("+str(i)+") > dt > span"
		baoyang_list_text = select_css(2,data,css,'')
		# print(baoyang_list_text+":::")

		css = "#package_baoyang > dl:nth-child("+str(i)+") > dd"
		dd_list = select_css(1,data,css,'')
		for j in range(2,len(dd_list)+2):
			# 拿到保养的子项
			css = "#package_baoyang > dl:nth-child("+str(i)+") > dd:nth-child("+str(j)+") > div > span"
			baoyang_text = select_css(2,data,css,'')
			# print(baoyang_text)
			# 做成字典{"子项":"保养类型"}
			baoyang_dict[baoyang_text] = baoyang_list_text

			css = "#package_baoyang > dl:nth-child("+str(i)+") > dd:nth-child("+str(j)+")"
			if "大保养服务" in baoyang_text:
				driver.find_element_by_css_selector(css).click()
			if "空调滤清器" in baoyang_text:
				driver.find_element_by_css_selector(css).click()
			if "火花塞" in baoyang_text:
				driver.find_element_by_css_selector(css).click()
			

	# print(baoyang_dict)
	# 数据更新到最新
	data = data_(driver)
	by_lx_open(driver,data,baoyang_dict)


def by_tuhu_baoyang_data(url_one):
	driver = webdriver.Chrome()
	driver.get(url_one)
	data = data_(driver)
	# 得到保养类型
	by_list(data,driver,url_one)


url = ["https://by.tuhu.cn/baoyang/VE-ZAR-Giulia/pl4.0T-n2019.html","https://by.tuhu.cn/baoyang/VE-ZAR-Giulia/pl2.0T-n2019.html","https://by.tuhu.cn/baoyang/VE-GM-S07BTHRV/pl1.6L-n2012.html","https://by.tuhu.cn/baoyang/VE-ZAR-Giulia/pl3.0T-n2019.html","https://by.tuhu.cn/baoyang/VE-McLaren540C/pl3.8T-n2019.html"]	

for url_one in url:
	by_tuhu_baoyang_data(url_one)

