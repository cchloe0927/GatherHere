import hashlib
import datetime

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session
import jwt
from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
from Oauth import Oauth
from models.User import User
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere

app.secret_key = SECRET_KEY


@app.route('/')
def index():
    return redirect(('/main'))

######령빈님 part
@app.route('/main')
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

@app.route('/main/movie', methods=['GET'])
def show_movie():
    show_movie = list(db.crawlingMovie.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_movie': show_movie})

@app.route('/main/book', methods=['GET'])
def show_book():
    show_book = list(db.crawlingBook.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_book': show_book})

@app.route('/main/album', methods=['GET'])
def show_album():
    show_album = list(db.crawlingAlbum.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_album': show_album})

@app.route("/search", methods=["GET"])
def search():
    keyword_receive = request.args.get('keyword')
    # print(keyword_receive)
    keyword = db.crawlingMovie.find_one({'title': {"$regex":keyword_receive+".*"}}, {'_id': False}) # movie check
    if keyword is None:
        keyword = db.crawlingBook.find_one({'title': {"$regex":keyword_receive+".*"}}, {'_id': False}) # book check
        if keyword is None:
            keyword = db.crawlingAlbum.find_one({'title': {"$regex": keyword_receive + ".*"}}, {'_id': False}) # album check
    # print(keyword)
    return jsonify({'keyword': keyword})

######현정님 part
# @app.route('/detail')
# def detail():
#     token_receive = request.cookies.get('Authorization')
#     temp = check(token_receive, 'username')
#     if temp['result']:
#         return render_template('detail.html', username=temp['data'])
#     else:
#         return render_template('detail.html')
#
# @app.route('/detail/info', methods=["GET"])
# def show_detail():
#     type = request.args.get('type') #type으로 조건 예외처리
#     id = request.args.get('id')
#     #print(type, id)
#
#     if type == "movie":
#         detail_id = db.crawlingMovie.find_one({'id': int(id)}, {'_id': False})
#     elif type == "book":
#         detail_id = db.crawlingBook.find_one({'id': int(id)}, {'_id': False})
#     else:
#         detail_id = db.crawlingAlbum.find_one({'id': int(id)}, {'_id': False})
#
#     return jsonify({'detailID': detail_id})
#
# @app.route("/detail/comment", methods=["POST"])
# def comment_post():
#     # comment 리스트에 고유 id 넣어주기 #comment 삭제 기능 구현
#     comment_list = list(db.comment.find({}, {'_id': False}))
#     commentId = len(comment_list) + 1
#
#     type = request.form['type']
#     contentId = request.form['id']
#     myStar = request.form['myStar']
#     text = request.form['text']
#     date = request.form['date']
#     title = request.form['title']
#     # print(type, contentId, myStar, myStar, text, date, title)
#
#     token_receive = request.cookies.get('Authorization')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"userid": payload['userid']})
#
#         doc = {
#             'id': user_info['userid'],  # 토큰에서 가져옴
#             'username': user_info['username'],  # 토큰에서 가져옴
#             'type': type,
#             'contentId': int(contentId),
#             'myStar': int(myStar),
#             'text': text,
#             'date': date,
#             'title': title,
#             'commentId': commentId,
#         }
#
#         if myStar == "0":
#             return jsonify({'msg': '나만의 평점을 선택해 주세요!'})
#         else:
#             db.comment.insert_one(doc)
#             return jsonify({'msg': '감상평이 등록되었습니다.'})
#
#     except jwt.ExpiredSignatureError:
#         print('만료')
#         return jsonify({'msg': '로그인이 만료되었습니다.'})
#     except jwt.exceptions.DecodeError:
#         print('오류')
#         return jsonify({'msg': '로그인이 필요한 작업입니다.'})
#
# @app.route("/detail/comment", methods=["GET"])
# def comment_get():
#     id = request.args.get('id')
#     comment_list = list(db.comment.find({'contentId': int(id)}, {'_id': False}))
#     comment_list.reverse()
#
#     token_receive = request.cookies.get('Authorization')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"userid": payload['userid']}, {'_id': False})
#         return jsonify({'comments': comment_list, 'user_info': user_info['userid']})
#     except jwt.ExpiredSignatureError:
#         print('만료')
#         return jsonify({'comments': comment_list, 'user_info': None})
#     except jwt.exceptions.DecodeError:
#         print('오류')
#         return jsonify({'comments': comment_list, 'user_info': None})
#
# @app.route("/detail/comment/delete", methods=["POST"])
# def delete_card():
#     commentId = request.form['commentId']
#     db.comment.delete_one({'commentId': int(commentId)})
#     return jsonify({'msg': '감상평이 삭제되었습니다.'})

#####정훈님 part
@app.route('/mypage')
def my_page():
    token_receive = request.cookies.get('Authorization')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']})
        print(user_info)
        print('try')
        return render_template('myPage.html', username=user_info["username"]) #로그인 되었을 때
    except jwt.ExpiredSignatureError:
        print('만료')
        return render_template("login.html", error="로그인 시간이 만료되었습니다.") # 로그인 만료 되었을 때
    except jwt.exceptions.DecodeError:
        print('오류')
        return render_template("login.html", error="로그인 정보가 존재하지 않습니다.") # 로그인 안되었거나 토큰이 글러먹엇을 때
@app.route('/mypage')
def my_page():
    token_receive = request.cookies.get('Authorization') 
    temp = check(token_receive, 'username')
    if temp['result']:
        return render_template('myPage.html', username=temp['data']) #로그인 되었을 때
    else:
        return render_template("login.html", error="로그인이 필요합니다.")  # 로그인 안되었거나 토큰이 글러먹엇을 때

@app.route("/mypage/bookmark/check", methods=["GET"]) # mypage 테스트
def check_get():
    token_receive = request.cookies.get('Authorization')

    temp = check(token_receive, 'userid')
    if temp['result'] is False:
        print('result')
        return jsonify({'logged': None})
    else:
        return jsonify({'logged':'wow!'})


@app.route("/mypage/bookmark", methods=["GET"])     
def bookmark_get():
    token_receive = request.cookies.get('Authorization')

    temp = check(token_receive, 'userid')
    if temp['result'] is False:
        return jsonify({'bookmarks': []}) # 북마크 없는 경우 공백으로 보내기
    user_id = temp['data']
    bookmark = db.users.find_one({'userid': user_id}, {'_id': False, 'bookmark': 1})
    bookmarks = bookmark['bookmark']
    datas = [] # 보내는 즐겨찾기 리스트 만들기
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


@app.route('/add_bookmark', methods=['POST'])
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


@app.route('/del_bookmark', methods=['POST'])
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

@app.route("/mypage/comment", methods=["GET"]) # 마이페이지 유저 커멘트 
def user_comment_get():
    token_receive = request.cookies.get('Authorization')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"userid": payload['userid']})

    comments = list(db.comment.find({'id': user_info['userid']}, {'_id': False})) 
    return jsonify({'comments': comments})


######로그인 관련 part
@app.route('/logintest')
def loginpage():
    token_receive = request.cookies.get('Authorization')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userid": payload['userid']})
        print(user_info)
        print('try')
        return render_template('test.html', username=user_info["username"])
    except jwt.ExpiredSignatureError:
        print('만료')
        return render_template("login.html", error="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        print('오류')
        return render_template("login.html", error="로그인 정보가 존재하지 않습니다.")
    # return render_template('test.html')

def example():

    token_receive = request.cookies.get('Authorization') #프론트에서 쿠키 전달 받는 곳
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)
        user_info = db.users.find_one({"userid": payload['userid']}) #추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기
        return render_template('test.html', username=user_info["username"]) #로그인이 되었을 때 작동하는곳
    except jwt.ExpiredSignatureError:
        print('만료')
        return render_template("login.html", error="로그인 시간이 만료되었습니다.") #로그인 만료 되었을때 (밑에 시간 다되었을 때랑 거의 비슷)
    except jwt.exceptions.DecodeError:
        print('오류')
        return render_template("login.html", error="로그인 정보가 존재하지 않습니다.") #로그인 오류 났을 때(로그인이 안되었을 때)


def check(token_receive, key):
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)

        user_info = db.users.find_one({"userid": payload['userid']}) #추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기
        return {'result':True, 'data' : user_info[key]}
    except jwt.ExpiredSignatureError:
        return {'result':False, 'data' : None}
    except jwt.exceptions.DecodeError:
        return {'result':False, 'data' : None}

@app.route('/kakao/login')
def kakao_sign_in():
    # 카카오톡으로 로그인 버튼을 눌렀을 때
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    print(kakao_oauth_url)
    return redirect(kakao_oauth_url)




@app.route('/kakao')
def kakao_login():
    # 카카오톡으로 로그인 버튼을 눌렀을 때
    return render_template('loginPage.html')

@app.route('/kakao/callback')
def kakao_callback():
    code = request.args.get("code")
    oauth = Oauth()
    auth_info = oauth.auth(code)
    # error 발생 시 로그인 페이지로 redirect
    if "error" in auth_info:
        return redirect('/login')

    # 아닐 시
    user = oauth.userinfo("Bearer " + auth_info['access_token'])

    kakao_account = user["kakao_account"]
    userid = user['id']
    profile = kakao_account["profile"]
    name = profile["nickname"]

    if "email" in kakao_account.keys():
        email = kakao_account["email"]
    else:
        email = f"{name}@kakao.com"

    # user = User.query.filter(User.name =name= name).first() #등록된 유저인지 확인
    user = db.users.find_one({'userid':userid})

    if user is None:
        # 유저 테이블에 추가
        user = User(userid=userid, username=name, email=email, password=hashlib.sha256(name.encode('utf-8')).hexdigest())
        db.users.insert_one(user.get_dic())

        message = '회원가입이 완료되었습니다.'

    session['isKakao'] = True
    # session['kakaoToken'] = auth_info['access_token']
    message = '로그인에 성공하였습니다.'
    payload = {
        'userid': userid,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)  # 유효시간, seconds 가 초단위로 진행 ex) 300 = 5분
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    response = make_response(redirect('/main'))
    response.set_cookie('Authorization', token)
    return response
@app.route('/logout')
def logout():
    if session['isKakao']:
        # auth = Oauth()
        # userid = auth.logout("Bearer " + session['kakaoToken'])
        # print(userid)
        kakao_logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={LOGOUT_REDIRECT_URI}"
        print(kakao_logout_url)
        return redirect(kakao_logout_url)

    else:
        return redirect('/main')
    # return redirect('/main')
# @app.route('/kakao/logout')
# def kakao_logout_url():
#     kakao_logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={LOGOUT_REDIRECT_URI}"
#     print(kakao_logout_url)
#     return redirect(kakao_logout_url)
@app.route('/signup', methods=['GET', 'POST'])  # GET(정보보기), POST(정보수정) 메서드 허용
def signup():
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('repassword')
        print(userid, username, password, password_2)
        if password != password_2:
            flash("입력한 비밀번호가 다릅니다.")
        elif db.users.find_one({'userid' : userid}) is not None:
            flash("동일한 id를 가진 계정이 존재합니다.")
        else:
            usertable = User(userid, username, email, password)
            db.users.insert_one(usertable.get_dic())
            return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        print(userid)
        print(db.users.find_one({'userid': userid}))
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        print(userid, password)
        if db.users.find_one({'userid': userid, 'password': password}) is not None:
            payload = {
                'userid': userid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = make_response(redirect('/main'))
            response.set_cookie('Authorization', token)
            session['isKakao'] = False
            return response
        else:
            return render_template('login.html', error='ID와 PassWord를 확인해주세요.')
    response = make_response(render_template('login.html'))
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)