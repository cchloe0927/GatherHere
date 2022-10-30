from flask import Flask, Blueprint, render_template, jsonify, request, redirect, make_response, flash, session
import jwt
from config import SECRET_KEY

from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere

bp = Blueprint('detail', __name__, url_prefix='/detail')
bp.secret_key = SECRET_KEY

def check(token_receive, key):
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)

        user_info = db.users.find_one({"userid": payload['userid']}) #추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기
        return {'result': True, 'data': user_info[key]}
    except jwt.ExpiredSignatureError:
        return {'result': False, 'data': None}
    except jwt.exceptions.DecodeError:
        return {'result': False, 'data': None}

@bp.route('/')
def detail():
    token_receive = request.cookies.get('Authorization')
    temp = check(token_receive, 'username')
    if temp['result']:
        return render_template('detail.html', username=temp['data'])
    else:
        return render_template('detail.html')

@bp.route('/info', methods=["GET"])
def show_detail():
    type = request.args.get('type') #type으로 조건 예외처리
    id = request.args.get('id')
    print(type, id)

    if type == "movie":
        detail_id = db.crawlingMovie.find_one({'id': int(id)}, {'_id': False})
    elif type == "book":
        detail_id = db.crawlingBook.find_one({'id': int(id)}, {'_id': False})
    else:
        detail_id = db.crawlingAlbum.find_one({'id': int(id)}, {'_id': False})

    return jsonify({'detailID': detail_id})

@bp.route("/comment", methods=["POST"])
def comment_post():
    # comment 리스트에 고유 id 넣어주기 #comment 삭제 기능 구현
    comment_list = list(db.comment.find({}, {'_id': False}))
    commentId = len(comment_list) + 1

    type = request.form['type']
    contentId = request.form['id']
    myStar = request.form['myStar']
    text = request.form['text']
    date = request.form['date']
    title = request.form['title']
    # print(type, contentId, myStar, myStar, text, date, title)

    token_receive = request.cookies.get('Authorization')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']})

        doc = {
            'id': user_info['userid'],  # 토큰에서 가져옴
            'username': user_info['username'],  # 토큰에서 가져옴
            'type': type,
            'contentId': int(contentId),
            'myStar': int(myStar),
            'text': text,
            'date': date,
            'title': title,
            'commentId': commentId,
        }

        if myStar == "0":
            return jsonify({'msg': '나만의 평점을 선택해 주세요!'})
        else:
            db.comment.insert_one(doc)
            return jsonify({'msg': '감상평이 등록되었습니다.'})

    except jwt.ExpiredSignatureError:
        print('만료')
        return jsonify({'msg': '로그인이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        print('오류')
        return jsonify({'msg': '로그인이 필요한 작업입니다.'})

@bp.route("/comment", methods=["GET"])
def comment_get():
    id = request.args.get('id')
    comment_list = list(db.comment.find({'contentId': int(id)}, {'_id': False}))
    comment_list.reverse()

    token_receive = request.cookies.get('Authorization')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']}, {'_id': False})
        return jsonify({'comments': comment_list, 'user_info': user_info['userid']})
    except jwt.ExpiredSignatureError:
        print('만료')
        return jsonify({'comments': comment_list, 'user_info': None})
    except jwt.exceptions.DecodeError:
        print('오류')
        return jsonify({'comments': comment_list, 'user_info': None})

@bp.route("/comment/delete", methods=["POST"])
def delete_card():
    commentId = request.form['commentId']
    db.comment.delete_one({'commentId': int(commentId)})
    return jsonify({'msg': '감상평이 삭제되었습니다.'})