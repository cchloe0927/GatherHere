import hashlib
import datetime

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session
import jwt
from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
from Oauth import Oauth
from models.User import User

import test, bookmark, detail, user, main, myPage

app = Flask(__name__)
#app.register_blueprint(test.bp) #예시
app.register_blueprint(user.bp)
app.register_blueprint(main.bp)
app.register_blueprint(detail.bp)
app.register_blueprint(myPage.bp)
app.register_blueprint(bookmark.bp) #즐겨찾기

app.secret_key = SECRET_KEY
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)