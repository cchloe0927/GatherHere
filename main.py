# from crypt import methods
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbGatherHere
# db = client.testdb

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
