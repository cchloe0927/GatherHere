from werkzeug.security import generate_password_hash

from config import CLIENT_ID, REDIRECT_URI
from Oauth import Oauth
from flask import Flask, redirect,render_template, request, session
from models.User import User

app = Flask(__name__)

@app.route('/')
def login():
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
    # 전달받은 authorization code를 통해서 access_token을 발급
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

@app.route('/signin', methods=['GET', 'POST'])  # GET(정보보기), POST(정보수정) 메서드 허용
def register():
    if request.method == 'GET':
        return render_template("signin.html")
    else:
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        password_2 = request.form.get('password')

        if not (userid and username and password and password_2):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            usertable = User(username)  # user_table 클래스
            usertable.userid = userid
            usertable.username = username
            usertable.password = password

            return redirect("/")


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)