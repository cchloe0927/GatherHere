import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

mongoUrl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoClient = MongoClient(mongoUrl)
db = mongoClient.dbGatherHere

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
mainData = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur', headers=headers)
mainsoup = BeautifulSoup(mainData.text, 'html.parser')

mains = mainsoup.select('#old_content > table > tbody > tr')
for main in mains:
    ranks = main.select_one('td:nth-child(1) > img')
    urls = main.select_one('td.title > div > a')
    stars = main.select_one('td.point')
    if (ranks is not None) and (urls is not None):
        rank = ranks['alt']
        url = urls['href']
        star = stars.text
        #print(rank, url, star)

        movieSoup = BeautifulSoup(requests.get('https://movie.naver.com' + url, headers=headers).text, 'html.parser')
        details = movieSoup.select('#content > div.article > div.mv_info_area')
        for detail in details:
            image = detail.select_one('div.poster > a > img')['src']
            title = detail.select_one('h3 > a').text
            genre = detail.select_one('div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a').text
            direction = detail.select_one('dl > dd:nth-child(4) > p > a').text
            actor = detail.select_one('dl > dd:nth-child(6) > p').text
            releasedata = detail.select('dl > dd:nth-child(2) > p > span:nth-child(4) >a')
            release = ""
            for i in range(2):
                release += releasedata[i].text
            #print([image, title, genre, release, direction, actor])

            # summary = soup.select_one(
            #     '#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text



####작업중####
# movieSoup = BeautifulSoup(requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=219812', headers=headers).text, 'html.parser')
#
# for i in range(1, 5):
#     details = movieSoup.find('dt', class_=('step'+str(i)))
#     if details is not None:
#         print(i)
#         if details.text == '개요()':
#             print(movieSoup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a').text)
#         elif details.text == '감독':
#             print(movieSoup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4)').text)
#         elif details.text == '출연':
#             print(movieSoup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p').text)
#         elif details.text == '등급':
#             print(movieSoup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child('+str(i*2)+') > p > a').text)

        # print("소제목", details.text)
        # print(movieSoup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child('+str(i*2)+') > p').text)
