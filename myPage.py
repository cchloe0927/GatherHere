from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbGatherHere

# @app.route("/bookmark", methods=["GET"])
# def bookmark_get():
#
#     # movie_list = list(db.movies.find({}, {'_id': False}))
#     # return jsonify({'movies':movie_list})

# markMovies = list(db.testuser.find({'id': user_id, 'bookmark.type': 'movie'}, {'_id': False, 'bookmark': 1}))
# markBooks = list(db.testuser.find({'id':user_id , 'bookmark.type':'book'},{'_id':False, 'bookmark':1}))
# markAlbums = list(db.testuser.find({'id':user_id , 'bookmark.type':'album'},{'_id':False, 'bookmark':1}))

def bookmark_list_get(user_id):
    bookmark = db.testuser.find_one({'id': user_id}, {'_id': False, 'bookmark': 1})
    bookmarks = bookmark['bookmark']

    datas = []
    for bm in bookmarks:
        if bm['type'] == 'movie':
            data = db.testmovie.find_one({'title': bm['content']}, {'_id': False})
            datas.append(data)
        elif bm['type'] == 'book':
            data = db.testbook.find_one({'title': bm['content']}, {'_id': False})
            datas.append(data)
        elif bm['type'] == 'album':
            data = db.testalbum.find_one({'title': bm['content']}, {'_id': False})
            datas.append(data)
    return datas

# comment = list(db.testcomment.find({'id': user_id}, {'_id': False}))


# detailMovie = list(db.testmovie.find({'title':list_movie['content']},{'_id':False, 'title':1}))


# print(detailMovie)



# result1 = mongo.find(filter={'$and':[{'name':'山田'},{'depId':'C0002'}]})
# db.restaurants.find({"address":{"building":"8825"}}).pretty()

# for i in comment:
#     print(i['title'])
#     print(i['text'])
#     print(i['username'])
#     print(i['date'])




# for user in users:
#     type = users[user]['bookmark']['type']
#     title = users[user]['bookmark']['content']
#     if title == 'movie':
#
#