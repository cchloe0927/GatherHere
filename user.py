import hashlib
import datetime

from flask import render_template,  request, redirect, make_response, flash, session, Blueprint
import jwt
from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
from Oauth import Oauth
from models.User import User

from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere


bp = Blueprint('user', __name__, url_prefix='/user')


# @bp.route('/logintest')
# def loginpage():
#     token_receive = request.cookies.get('Authorization')
#     print(token_receive)
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"userid": payload['userid']})
#         print(user_info)
#         print('try')
#         return render_template('test.html', username=user_info["username"])
#     except jwt.ExpiredSignatureError:
#         print('만료')
#         return render_template("login.html", error="로그인 시간이 만료되었습니다.")
#     except jwt.exceptions.DecodeError:
#         print('오류')
#         return render_template("login.html", error="로그인 정보가 존재하지 않습니다.")
#     # return render_template('test.html')


def check(token_receive, key):
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #쿠키에 있는 jwt 인코딩(쿠키에 있는 데이터 추출하는 곳)

        user_info = db.users.find_one({"userid": payload['userid']}) #추출한 데이터가 DB에 존재하는지 확인하고 해당 데이터를 user_info에 넣기
        return {'result':True, 'data' : user_info[key]}
    except jwt.ExpiredSignatureError:
        return {'result':False, 'data' : None}
    except jwt.exceptions.DecodeError:
        return {'result':False, 'data' : None}

@bp.route('/kakao/login')
def kakao_sign_in():
    # 카카오톡으로 로그인 버튼을 눌렀을 때
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
    print(kakao_oauth_url)
    return redirect(kakao_oauth_url)




# @bp.route('/kakao')
# def kakao_login():
#     # 카카오톡으로 로그인 버튼을 눌렀을 때
#     return render_template('loginPage.html')

@bp.route('/kakao/callback')
def kakao_callback():
    code = request.args.get("code")
    oauth = Oauth()
    auth_info = oauth.auth(code)
    # error 발생 시 로그인 페이지로 redirect
    if "error" in auth_info:
        return redirect('user/login')

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
    response = make_response(redirect('/'))
    response.set_cookie('Authorization', token)
    return response
@bp.route('/logout')
def logout():
    if session['isKakao']:
        # auth = Oauth()
        # userid = auth.logout("Bearer " + session['kakaoToken'])
        # print(userid)
        kakao_logout_url = f"https://kauth.kakao.com/oauth/logout?client_id={CLIENT_ID}&logout_redirect_uri={LOGOUT_REDIRECT_URI}"
        print(kakao_logout_url)
        return redirect(kakao_logout_url)

    else:
        return redirect('/')
    # return redirect('/main')
@bp.route('/signup', methods=['GET', 'POST'])  # GET(정보보기), POST(정보수정) 메서드 허용
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
            return redirect('/user/login')

    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    print('??')
    if request.method == 'POST':
        userid = request.form['userid']
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        if db.users.find_one({'userid': userid, 'password': password}) is not None:
            payload = {
                'userid': userid,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = make_response(redirect('/'))
            print('??')
            print(redirect('/'))
            response.set_cookie('Authorization', token)
            session['isKakao'] = False
            return response
        else:
            return render_template('login.html', error='ID와 PassWord를 확인해주세요.')
    response = make_response(render_template('login.html'))
    return response


