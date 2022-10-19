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

#http://localhost:5000/detail?type=movie&id=187831
#http://localhost:5000/detail?type=book&id=187831
#http://localhost:5000/detail?type=album&id=187831

@app.route('/detail/info', methods=["GET"])
def show_detail_get():
    type = request.args.get('type') #if나중에
    id = request.args.get('id')
    print(type, id)
    detail_id = db.testmovie.find_one({'id': int(id)}, {'_id': False})
    print(detail_id)
    return jsonify({'detailID': detail_id})

@app.route("/detail/comment", methods=["POST"])
def comment_post():
    # id = request.form['id']
    # username = request.form['username']

    type = request.form['type']
    contentId = request.form['id']
    myStar = request.form['myStar']
    text = request.form['text']
    date = request.form['date']

    doc = {
        'id': '임시테스트UserID',  #이후에 db find이후 데이터 입력
        'username': '이현정', #이후에 db find이후 데이터 입력
        'type': type,
        'contentId': int(contentId),
        'myStar': myStar,
        'text': text,
        'date': date,
    }
    db.testcomment.insert_one(doc)
    return jsonify({'msg':'감상평이 등록되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
