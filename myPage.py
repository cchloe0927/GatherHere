from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

mongourl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoclient = MongoClient(mongourl)
db = mongoclient.dbGatherHere

@app.route('/')
def home():
    return render_template('myPage.html')

@app.route("/bookmark", methods=["GET"])
def bookmark_get():
    user_id = 'test1234'
    bookmark = db.testuser.find_one({'id': user_id}, {'_id': False, 'bookmark': 1})
    bookmarks = bookmark['bookmark']

    datas = []
    for bm in bookmarks:
        if bm['type'] == 'movie':
            data = db.testmovie.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'movie'
            print(data['type'])
            datas.append(data)
        elif bm['type'] == 'book':
            data = db.testbook.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'book'
            print(data['type'])
            datas.append(data)
        elif bm['type'] == 'album':
            data = db.testalbum.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'album'
            datas.append(data)

    return jsonify({'bookmarks': datas})

@app.route("/comment", methods=["GET"])
def comment_get():
    user_id = 'test1234'
    comments = list(db.testcomment.find({'id': user_id}, {'_id': False}))
    return jsonify({'comments':comments})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
