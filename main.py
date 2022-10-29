# from flask import Flask, render_template, request, jsonify
import imp
from flask import Blueprint, render_template, request, jsonify
from config import SECRET_KEY
import jwt
# app = Flask(__name__)
from pymongo import MongoClient
bp = Blueprint('main', __name__, url_prefix='/')

client = MongoClient(
    'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbGatherHere

@bp.route('/')
def main():
    token_receive = request.cookies.get('Authorization')  # 프론트에서 쿠키 전달 받는 곳
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])  # 쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)
        user_info = db.users.find_one({"userid": payload['userid']})  # 추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기

        return render_template('main.html', username=user_info['username']) # 로그인이 되었을 때 작동하는곳
    except jwt.ExpiredSignatureError:
        print('만료')
        return render_template("main.html")  # 로그인 만료 되었을때 (밑에 시간 다되었을 때랑 거의 비슷)
    except jwt.exceptions.DecodeError:
        print('오류')
        return render_template("main.html")  # 로그인 오류 났을 때(로그인이 안되었을 때)

@bp.route('/movie', methods=['GET'])
def show_movie():
    show_movie = list(db.crawlingMovie.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_movie': show_movie})

@bp.route('/book', methods=['GET'])
def show_book():
    show_book = list(db.crawlingBook.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_book': show_book})

@bp.route('/album', methods=['GET'])
def show_album():
    show_album = list(db.crawlingAlbum.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_album': show_album})

#검색
@bp.route("/search", methods=["GET"])
def search():
    keyword_receive = request.args.get('keyword')
    print(keyword_receive)
    keyword = db.crawlingMovie.find_one({'title': {"$regex":keyword_receive+".*"}}, {'_id': False}) # movie check
    if keyword is None:
        keyword = db.crawlingBook.find_one({'title': {"$regex":keyword_receive+".*"}}, {'_id': False}) # book check
        if keyword is None:
            keyword = db.crawlingAlbum.find_one({'title': {"$regex": keyword_receive + ".*"}}, {'_id': False}) # album check
    # print(keyword)
    return jsonify({'keyword': keyword})
# if __name__ == '__main__':
#     bp.run('0.0.0.0', port=5000, debug=True)
