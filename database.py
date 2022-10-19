from pymongo import MongoClient
url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url)
db = client.dbGatherHere



movie = {
    'id':187821,
    'title': '인생은 아름다워',
    'rank':1,
    'image': 'https://movie.naver.com/movie/bi/mi/basic.naver?code=187821#',
    'direction': '최국희',
    'actor': '류승룡(강진봉), 염정아(오세연), 박세완(여고생 세연)',
    'ageLimit': '12세',
    'release': '2022.09.28',
    'summary':'무뚝뚝한 남편 \‘진봉\’과 무심한 아들 딸을 위해 헌신하며 살아온 ‘세연’은',
    'star' : 8.36

}
# db.testmovie.insert_one(movie)
# movietest = db.testmovie.find_one({'rank' : 1})
# print(movietest)

book = {
    'id' : 301692224,
    'title': '트렌드 코리아 2023',
    'rank' : 1,
    'author' : '김난도,전미영,최지혜,이수진,권정윤,이준영,이향은,한다혜,이혜원,추예린 (지은이)',
    'release' : '2022.10.05',
    'summary' : '작년 이맘때 출간된 <트렌드 코리아 2022>는 당시 2년여 동안 계속되는 팬데믹 상황에서도 "우리를 죽이지 못하는',
    'star' : 7.0
}
# db.testbook.insert_one(book)

album = {
    'id':303079221,
    'title' : '스트레이 키즈 - 미니앨범 MAXIDENT (CASE ver.)',
    'rank' : 1,
    'artist' : '스트레이 키즈 (Stray Kids)',
    'release' : '2022.10',
    'star' : 10,
    'company' : 'JYP 엔터테인먼트',

}
# db.testalbum.insert_one(album)

comment = {
    'id':'test1234',
    'type' : 'movie',
    'title' : '인생은 아름다워',
    'text' : '재밌어용',
    'username': '밤준',
    'myStar':7,
    'date':'2022.10.18'
}
# db.testcomment.insert_one(comment)
user = {
    'id' : 'test1234',
    'username' : '밤준',
    'password' : 'qwer1234',
    'bookmark' : [{'type':'movie', 'content':'인생은 아름다워'}, {'type':'book', 'content':'트렌드 코리아 2023'}]
}

# doc = {
#         'id': 'userId',
#         'username': '이현정',
#         'type': 'movie',
#         'title': '인생은 아름다워',
#         'myStar': myStar,
#         'text': text,
#         'date': date,
#     }
db.testcomment.insert_one(doc)
db.testuser.insert_one(user)