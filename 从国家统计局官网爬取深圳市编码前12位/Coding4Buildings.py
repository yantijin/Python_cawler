import requests
from lxml import etree
from bs4 import BeautifulSoup

base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/44/"
add_part = "4403.html"
url = base_url + add_part

headers = {"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"}

response = requests.get(url, headers = headers)

# print(response.content)
# 得到html界面的内容
html = response.text
selector = etree.HTML(html)
lianjie = selector.xpath('//a/@href')
#print(lianjie)
#htmls = list(set(lianjie))
first_htmls = sorted(set(lianjie),key = lianjie.index)
# 去除掉最后一个无用的链接
del first_htmls[len(first_htmls)-1]


file_obj = open('coding4buildings.txt','w')




# print(htmls)
for new_html in first_htmls:
	new_url = base_url + new_html
	new_res = requests.get(new_url,headers=headers)
	# 第二级的html文档
	second_html = new_res.text
	second_selector = etree.HTML(second_html)
	second_lianjie = second_selector.xpath('//a/@href')
	second_htmls = sorted(set(second_lianjie), key = second_lianjie.index)

	del second_htmls[len(second_htmls)-1]
	# print(second_htmls)
	for j in second_htmls:
		n_url = base_url + '03/'+j
		print(n_url)
		n_res = requests.get(n_url,headers = headers)
		# 第三级的文档
		third_html = n_res.text
		soup = BeautifulSoup(third_html, 'lxml')
		body = soup.body
		# print(body)
		pp = body.find_all('tr',class_ = 'villagetr')
		# print(pp)
		# 输出编码
		for i in pp:
			file_obj.write(i.find('td').string)
			file_obj.write('\n')


file_obj.close()








