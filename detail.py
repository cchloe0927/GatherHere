from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/info', methods=["GET"])
def show_detail_get():
    type = request.args.get('type') #type으로 조건 예외처리
    id = request.args.get('id')
    #print(type, id)

    if type == "movie":
        detail_id = db.testmovie.find_one({'id': int(id)}, {'_id': False})
    elif type == "book":
        detail_id = db.testbook.find_one({'id': int(id)}, {'_id': False})
    else:
        detail_id = db.testalbum.find_one({'id': int(id)}, {'_id': False})

    return jsonify({'detailID': detail_id})

@app.route("/detail/comment", methods=["POST"])
def comment_post():
    # comment 리스트에 고유 id 넣어주기 #comment 삭제 기능 구현
    comment_list = list(db.testcomment.find({}, {'_id': False}))
    commentId = len(comment_list) + 1

    # id = request.form['id']
    # username = request.form['username']

    type = request.form['type']
    contentId = request.form['id']
    myStar = request.form['myStar']
    text = request.form['text']
    date = request.form['date']
    title = request.form['title']

    doc = {
        'id': '임시테스트UserID',  #이후에 db find이후 데이터 입력
        'username': '이현정', #이후에 db find이후 데이터 입력
        'type': type,
        'contentId': int(contentId),
        'myStar': int(myStar), 
        'text': text,
        'date': date,
        'title': title,
        'commentId': commentId,
    }
    db.testcomment.insert_one(doc)
    return jsonify({'msg':'감상평이 등록되었습니다.'})

@app.route("/detail/comment", methods=["GET"])
def comment_get():
    id = request.args.get('id')
    print(id)
    comment_list = list(db.testcomment.find({'contentId': int(id)}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/detail/comment/delete", methods=["POST"])
def delete_card():
    commentId = request.form['commentId']
    db.testcomment.delete_one({'commentId': int(commentId)})
    return jsonify({'msg': '감상평이 삭제되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
