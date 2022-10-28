from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session, Blueprint
import jwt
from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI


from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere

bp = Blueprint('bookmark', __name__, url_prefix='/bookmark')


@bp.route("/", methods=["GET"])
def bookmark_get():
    token_receive = request.cookies.get('Authorization')

    temp = check(token_receive, 'userid')
    if temp['result'] is False:
        return jsonify({'bookmarks': []})
    user_id = temp['data']
    bookmark = db.users.find_one({'userid': user_id}, {'_id': False, 'bookmark': 1})
    bookmarks = bookmark['bookmark']
    datas = []
    for bm in bookmarks:
        if bm['type'] == 'movie':
            data = db.crawlingMovie.find_one({'id': int(bm['id'])}, {'_id': False})
            # data['type'] = 'movie'
            datas.append(data)
        elif bm['type'] == 'book':
            data = db.crawlingBook.find_one({'id': int(bm['id'])}, {'_id': False})
            # data['type'] = 'book'
            datas.append(data)
        elif bm['type'] == 'album':
            data = db.crawlingAlbum.find_one({'id': int(bm['id'])}, {'_id': False})
            # data['type'] = 'album'
            datas.append(data)
    return jsonify({'bookmarks': datas})

@bp.route('/add', methods=['POST'])
def add_bookmark():
    token_receive = request.cookies.get('Authorization')
    type = request.form.get('type')
    id = request.form.get('id')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']})
        bookmark = user_info['bookmark']
        bookmark.append({'type':type, 'id':int(id)})
        db.users.update_one({'userid':user_info['userid']}, {'$set':{'bookmark':bookmark}})
        print('?')
        return jsonify({'result':'success'})
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail'})


@bp.route('/del', methods=['POST'])
def del_bookmark():
    token_receive = request.cookies.get('Authorization')
    type = request.form.get('type')
    id = int(request.form.get('id'))
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']})
        bookmark = user_info['bookmark']
        del bookmark[bookmark.index({'type':type, 'id':int(id)})]
        db.users.update_one({'userid':user_info['userid']}, {'$set':{'bookmark':bookmark}})
        return jsonify({'result':'success'})
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail'})

def check(token_receive, key):
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])  # 쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)

        user_info = db.users.find_one(
            {"userid": payload['userid']})  # 추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기
        return {'result': True, 'data': user_info[key]}
    except jwt.ExpiredSignatureError:
        return {'result': False, 'data': None}
    except jwt.exceptions.DecodeError:
        return {'result': False, 'data': None}