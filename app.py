from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()

url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile=ca)
db = client.dbGatherHere

######령빈님 part
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/main/movie', methods=['GET'])
def show_movie():
    show_movie = list(db.crawlingMovie.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_movie': show_movie})

@app.route('/main/book', methods=['GET'])
def show_book():
    show_book = list(db.crawlingBook.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_book': show_book})

@app.route('/main/album', methods=['GET'])
def show_album():
    show_album = list(db.crawlingalbum.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_album': show_album})

######현정님 part
@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/info', methods=["GET"])
def show_detail():
    type = request.args.get('type') #type으로 조건 예외처리
    id = request.args.get('id')
    print(type, id)

    if type == "movie":
        detail_id = db.crawlingMovie.find_one({'id': int(id)}, {'_id': False})
        print(detail_id)
    elif type == "book":
        detail_id = db.crawlingBook.find_one({'id': int(id)}, {'_id': False})
        print(detail_id)
    else:
        detail_id = db.crawlingalbum.find_one({'id': int(id)}, {'_id': False})

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
    #print(type, contentId, myStar, myStar, text, date, title)

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
    if myStar == "0":
        return jsonify({'msg': '나만의 평점을 선택해 주세요!'})
    else:
        db.testcomment.insert_one(doc)
        return jsonify({'msg': '감상평이 등록되었습니다.'})

@app.route("/detail/comment", methods=["GET"])
def comment_get():
    id = request.args.get('id')
    #print(id)
    comment_list = list(db.testcomment.find({'contentId': int(id)}, {'_id': False}))
    return jsonify({'comments': comment_list})

@app.route("/detail/comment/delete", methods=["POST"])
def delete_card():
    commentId = request.form['commentId']
    db.testcomment.delete_one({'commentId': int(commentId)})
    return jsonify({'msg': '감상평이 삭제되었습니다.'})


######정훈님 part
@app.route('/mypage')
def my_page():
    return render_template('myPage.html')

@app.route("/mypage/bookmark", methods=["GET"])
def bookmark_get():
    user_id = 'test1234'
    bookmark = db.testuser.find_one({'id': user_id}, {'_id': False, 'bookmark': 1})
    bookmarks = bookmark['bookmark']

    datas = []
    for bm in bookmarks:
        if bm['type'] == 'movie':
            data = db.testmovie.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'movie'
            print(data['type'])
            datas.append(data)
        elif bm['type'] == 'book':
            data = db.testbook.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'book'
            print(data['type'])
            datas.append(data)
        elif bm['type'] == 'album':
            data = db.testalbum.find_one({'title': bm['content']}, {'_id': False})
            data['type'] = 'album'
            datas.append(data)

    return jsonify({'bookmarks': datas})

@app.route("/mypage/comment", methods=["GET"])
def user_comment_get():
    user_id = '임시테스트UserID'
    comments = list(db.testcomment.find({'id': user_id}, {'_id': False}))
    return jsonify({'comments': comments})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)