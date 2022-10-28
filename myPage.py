import hashlib
import datetime

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session
import jwt
from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
from Oauth import Oauth
from models.User import User
from pymongo import MongoClient


mypage = Flask(__name__)
mypage.register_blueprint(mypage.bp) #이런식으로 등록

mongourl = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
mongoclient = MongoClient(mongourl)
db = mongoclient.dbGatherHere


@mypage.route('/')
def home():
    return render_template('myPage.html')

@mypage.route("/bookmark", methods=["GET"])
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

@mypage.route("/comment", methods=["GET"])
def user_comment_get():
    token_receive = request.cookies.get('Authorization')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"userid": payload['userid']})

    comments = list(db.comment.find({'id': user_info['userid']}, {'_id': False}))
    return jsonify({'comments': comments})
