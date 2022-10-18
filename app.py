import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code=187821', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

#content > div.article > div.mv_info_area
#content > div.article > div.mv_info_area > div.poster > a > img
#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)
#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2)
#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4)
#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a
#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(6) > p
#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a

details = soup.select('#content > div.article > div.mv_info_area')
for detail in details:
    poster = detail.select_one('div.poster > a > img')['src']
    title = detail.select_one('h3 > a').text
    release = "".join(detail.select_one('dl > dd:nth-child(2) > p > span:nth-child(4)').text.strip().split('\n'))
    director = detail.select_one('dl > dd:nth-child(4) > p > a').text
    actor = detail.select_one('dl > dd:nth-child(6) > p').text
    ageLimit = detail.select_one('dl > dd:nth-child(8) > p > a').text
    print(poster, title, release, director, actor, ageLimit)

summary = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text
#print(summary)