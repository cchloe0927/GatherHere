import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()

mongoUrl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoClient = MongoClient(mongoUrl, tlsCAFile=ca)
db = mongoClient.dbGatherHere

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
mainData = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur', headers=headers)
mainsoup = BeautifulSoup(mainData.text, 'html.parser')

datas = []

mains = mainsoup.select('#old_content > table > tbody > tr')
for main in mains:
    ranks = main.select_one('td:nth-child(1) > img')
    urls = main.select_one('td.title > div > a')
    stars = main.select_one('td.point')
    if (ranks is not None) and (urls is not None):
        rank = ranks['alt']
        url = urls['href']
        id = url.split('=')[1]
        star = stars.text
        # print(rank, url, star, id)

        movieSoup = BeautifulSoup(requests.get('https://movie.naver.com' + url, headers=headers).text, 'html.parser')
        detail = movieSoup.select_one('#content > div.article > div.mv_info_area')
        image = detail.select_one('div.poster > a > img')['src']
        title = detail.select_one('h3 > a').text
        genre = detail.select_one('div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a').text
        direction = detail.select_one('dl > dd:nth-child(4) > p > a').text
        actor = detail.select_one('dl > dd:nth-child(6) > p').text.replace('\t', '').replace('\r', '').replace('\n', '')
        releasedata = detail.select('dl > dd:nth-child(2) > p > span:nth-child(4) >a')
        release = ""
        for i in range(2):
            release += releasedata[i].text

        summary = movieSoup.select_one(
            '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text
        # print(image, title, genre, release, direction, actor)
        # print(summary)

        datas.append(
            {
                'id': int(id),
                'image': image,
                'rank': rank,
                'title': title,
                'star': star,
                'release': release,
                'genre': genre,
                'direction': direction,
                'actor': actor,
                'summary': summary,
                'type': 'movie'
            }
        )
db.crawlingMovie.delete_many({})
db.crawlingMovie.insert_many(datas)
