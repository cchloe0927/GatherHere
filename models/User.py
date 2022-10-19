from werkzeug.security import generate_password_hash, check_password_hash

class User():  # 데이터 모델을 나타내는 객체 선언
    def __init__(self, userid, username, password):
        self.userid = userid
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_dic(self):
        return ({'username':self.username,
                         'email':self.email,
                         'password':self.password})