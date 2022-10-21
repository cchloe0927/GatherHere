import datetime
import hashlib

from werkzeug.security import generate_password_hash

from config import CLIENT_ID, REDIRECT_URI, SECRET_KEY
from Oauth import Oauth
from flask import Flask, redirect, render_template, request, session, flash, jsonify, url_for
from models.User import User
from pymongo import MongoClient
import jwt
url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url)
pymongodb = client.dbGatherHere

app = Flask(__name__)
app.secret_key = SECRET_KEY
@app.route('/')
def loginpage():
    return render_template('loginPage.html')

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
    print(code)
    oauth = Oauth()
    auth_info = oauth.auth(code)

    # error 발생 시 로그인 페이지로 redirect
    if "error" in auth_info:
        print("에러가 발생했습니다.")
        return {'message': '인증 실패'}, 404

    # 아닐 시
    user = oauth.userinfo("Bearer " + auth_info['access_token'])

    print(user)
    kakao_account = user["kakao_account"]
    profile = kakao_account["profile"]
    name = profile["nickname"]
    if "email" in kakao_account.keys():
        email = kakao_account["email"]
    else:
        email = f"{name}@kakao.com"

    # user = User.query.filter(User.name =name= name).first() #등록된 유저인지 확인

    if user is None:
        # 유저 테이블에 추가
        user = User(name, email, generate_password_hash(name))
        # db.testuser.insert(user)

        message = '회원가입이 완료되었습니다.'
        value = {"status": 200, "result": "success", "msg": message}

    session['email'] = user.email
    session['isKakao'] = True
    message = '로그인에 성공하였습니다.'
    value = {"status": 200, "result": "success", "msg": message}

    return redirect("/")

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
        elif pymongodb.testuser.find_one({'userid' : userid}) is not None:
            flash("동일한 id를 가진 계정이 존재합니다.")
        else:
            usertable = User(userid, username, email, password)
            pymongodb.testuser.insert_one(usertable.get_dic())
            return redirect('/login')
    else:
        session.pop('_flashes', None)
    return render_template('signup.html')

@app.route('/signup/check', methods=['GET'])  # GET(정보보기), POST(정보수정) 메서드 허용
def check_id():
    userid = request.args.get('userid')
    print(userid)
    if pymongodb.testuser.find_one({'userid':userid}) == None:
        result = {'result': 'success', 'msg': '햅격'}
    else:
        result = {'result': 'fail', 'msg': '동일한 id를 가진 계정이 존재합니다.'}
    return jsonify(result)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        print(userid)
        print(pymongodb.testuser.find_one({'userid': userid}))
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        print(userid, password)
        if  pymongodb.testuser.find_one({'userid':userid, 'password':password}) is not None:
            payload = {
                'userid' : userid,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=5) #유효시간
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'result': 'success', 'token': token})
        else:
            return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
    return render_template('loginPage.html')


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)

# def check_token():
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = pymongodb.testuser.find_one({"userid": payload['userid']})
#         return render_template('index.html', nickname=user_info["nick"])
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
