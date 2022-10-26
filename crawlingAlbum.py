import requests
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient

mongoUrl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoClient = MongoClient(mongoUrl)
db = mongoClient.dbGatherHere

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=2', headers=headers)
context = ssl._create_unverified_context()
res = urlopen('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=MonthlyBest', context=context)
soup = BeautifulSoup(data.text, 'html.parser')

datas = []

titles = soup.select("a.bo3")
ranks = soup.select('#Myform > div > table > tr > td:nth-child(1) > table > tr:nth-child(1) > td > div')
artists = soup.select(
    '#Myform > div > table > tr > td:nth-child(3) > table > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > ul > li > a:nth-child(1)')

for i in range(50):
    title = titles[i].text.split('[버')[0]
    rank = int(ranks[i].text.strip('.'))
    artist = artists[i].text
    url = titles[i].get('href')
    content_id = int(url.split('=')[1])

    data_d = requests.get(url, headers=headers)
    soup_d = BeautifulSoup(data_d.text, 'html.parser')

    image = soup_d.select_one("#CoverMainImage").get('src')

    company = soup_d.select_one('li.Ere_sub2_title > a:nth-child(3)').text
    info = soup_d.select_one('li.Ere_sub2_title').text.split("-")
    release = info[0][-4:] + "." + info[1] + "." + info[2][:2]

    star = float(soup_d.select_one('a.Ere_sub_pink.Ere_fs16.Ere_str').text.strip())

    genre = soup_d.select_one('#ulCategory > li > a:nth-child(3) > b').text

    datas.append(
        {'id': content_id,
         'title': title,
         'image': image,
         'artist': artist,
         'company': company,
         'release': release,
         'star': star,
         'genre': genre,
         'rank': rank,
         'type': 'album'}
    )
    print(rank, content_id, title, release, star, genre)

# db.crawlingalbum.delete_many({})
# db.crawlingalbum.insert_many(datas)
