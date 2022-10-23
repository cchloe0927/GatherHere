import datetime
import hashlib

from werkzeug.security import generate_password_hash

from config import CLIENT_ID, REDIRECT_URI, SECRET_KEY
from Oauth import Oauth
from flask import Flask, redirect, render_template, request, session, flash, jsonify, make_response, url_for
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
    token_receive = request.cookies.get('Authorization')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        payload['userid']
        user_info = pymongodb.testuser.find_one({"userid": payload['userid']})
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
        return redirect('/login')

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
    user = pymongodb.testuser.find_one({'userid':name})

    if user is None:
        # 유저 테이블에 추가
        print('추가')
        user = User(userid=email, username=name, email=email, password=hashlib.sha256(name.encode('utf-8')).hexdigest())
        print(user)
        pymongodb.testuser.insert_one(user.get_dic())

        message = '회원가입이 완료되었습니다.'

    # session['email'] = user.email
    # session['isKakao'] = True
    message = '로그인에 성공하였습니다.'
    payload = {
        'userid': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)  # 유효시간, seconds 가 초단위로 진행 ex) 300 = 5분
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    result = {'result': 'success', 'token': token, 'username': pymongodb.testuser.find_one({'userid': email})['username']}
    session['access'] = result
    response = make_response(redirect('/'))
    response.set_cookie('Authorization', token)
    return response

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

    return render_template('signup.html')

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
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            result = {'result': 'success', 'token': token, 'username':pymongodb.testuser.find_one({'userid':userid})['username']}
            response = make_response(redirect('/'))
            response.set_cookie('Authorization',token)
            return response
        else:
            return render_template('login.html', error='ID와 PassWord를 확인해주세요.')
    response = make_response(render_template('login.html'))
    return response

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('/')


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)

# def check_token(token_receive):

