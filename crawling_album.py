import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

mongoUrl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoClient = MongoClient(mongoUrl)
db = mongoClient.dbGatherHere

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=2',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
#Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(2) > a > b

# movies = soup.select('#old_content > table > tbody > tr')

#Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div
#Myform > div:nth-child(4) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > div

#Myform > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(1)

# title = soup.select_one("a.bo3")
# rank = soup.select_one('#Myform > div > table > tr > td:nth-child(1) > table > tr:nth-child(1) > td > div')
# artist = soup.select_one('#Myform > div:nth-child(3) > table > tr > td:nth-child(3) > table > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li:nth-child(3) > a:nth-child(1)')
# print(title.text)
# print(rank.text)
# print(artist.text)
# url = title.get('href')
# print(url)
# print(url.split('=')[1])

url='https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=303301299'

data_d = requests.get(url ,headers=headers)
soup_d = BeautifulSoup(data_d.text, 'html.parser')

image = soup_d.select_one("#CoverMainImage")
print(image.get('src'))
#Ere_prod_allwrap > div.Ere_prod_topwrap > div.Ere_prod_titlewrap > div.left > div > ul > li.Ere_sub2_title

info = soup_d.select_one('li.Ere_sub2_title').text.split("-")
release = info[0][-4:]+"."+info[1]+"."+info[2][:2]
print(release)

#wa_product_top1_wa_Top_Ranking_pnlRanking > div.info_list.Ere_fs15.Ere_ht18 > a.Ere_sub_pink.Ere_fs16.Ere_str
star = soup_d.select_one('a.Ere_sub_pink.Ere_fs16.Ere_str')
print(star.text)
#ulCategory > li > a:nth-child(3) > b
genre = soup_d.select_one('#ulCategory > li > a:nth-child(3) > b')
print(genre.text)
#Ere_prod_allwrap > div.Ere_prod_middlewrap > div:nth-child(15) > div.Ere_prod_mconts_R
#
# summary = soup_d.select_one('div.Ere_prod_middlewrap > div.Ere_prod_mconts_box')
# print(summary)

# for i in titles:
#     print(i.text)
#     url = i.get('href')
#     print(url)
#     print(url.split('=')[1])

