from flask import Flask, render_template, make_response, request
app = Flask(__name__)


@app.route('/')
def home():
    a = make_response(render_template('test.html'))
    a.set_cookie('test', 'gaterhere')
    return a

@app.route('/test')
def test():
    cookie = request.cookies.get('test')
    print(cookie)
    return render_template('test.html')
if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)