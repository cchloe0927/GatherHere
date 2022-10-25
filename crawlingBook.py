import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

mongoUrl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoClient = MongoClient(mongoUrl)
db = mongoClient.dbGatherHere

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(
    'https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&BestType=MonthlyBest', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

datas = []

books = soup.select(
    '#Myform > div > table > tr')

for book in books:
    title = book.select_one(
        'td > table > tr > td > div > ul > li > a > b')
    if title is not None:
        title = title.text.split('(')[0].strip()
    author = book.select_one(
        'td > table > tr> td > div > ul > li:nth-child(3)').text.split('|')[0].strip()
    if '%' in author:
        author = book.select_one(
            'td > table > tr> td > div > ul > li:nth-child(2)').text.split('|')[0].strip()
    rank = int(book.select_one(
        'td:nth-child(1) > table > tr:nth-child(1) > td > div').text.split('.')[0])
    image = book.select_one('.i_cover')['src']
    url = book.select_one(
        'td > table > tr > td > div > ul > li:nth-child(2) > a')['href']
    if 'Search' in url:
        url = book.select_one(
            'td > table > tr > td > div > ul > li:nth-child(1) > a')['href']
    book_id = int(url.split('ItemId=')[1])
    data_d = requests.get(url, headers=headers)
    soup_d = BeautifulSoup(data_d.text, 'html.parser')
    star = float(soup_d.select_one('a.Ere_sub_pink.Ere_fs16.Ere_str').text)
    genre = soup_d.select_one('#ulCategory > li > a:nth-child(2)').text
    summary = soup_d.select_one(
        'div:nth-child(4) > div.Ere_prod_mconts_R')
    if summary is not None:
        summary = summary.text.strip()[1:240] + '...'
    elif summary is None:
        summary = '책소개가 없습니다😢'
    else:
        summary = '책소개가 없습니다😢'
    release = soup_d.select_one(
        'div > ul > li.Ere_sub2_title').text.split()[-1][-10:]
    datas.append(
        {'id': book_id,
         'title': title,
         'image': image,
         'author': author,
         'release': release,
         'summary': summary,
         'star': star,
         'genre': genre,
         'rank': rank,
         'type': 'book'}
    )
    print(rank, book_id, title, author, release, star, genre)

db.crawlingBook.delete_many({})
db.crawlingBook.insert_many(datas)
