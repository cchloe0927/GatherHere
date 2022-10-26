import hashlib

from werkzeug.security import generate_password_hash, check_password_hash

class User():  # 데이터 모델을 나타내는 객체 선언
    def __init__(self, userid, username, email, password):
        self.userid = userid
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def get_dic(self):
        return ({'userid':self.userid,
                 'username':self.username,
                 'email':self.email,
                 'password':self.password,
                 'bookmark':[]})

    def set_dic(self, dic):
        self.userid = dic['id']
        self.username = dic['username']
        self.email = dic['email']
        self.password = dic['password']