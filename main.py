# from flask import Flask, render_template, request, jsonify
from flask import Blueprint, render_template, request, jsonify
# app = Flask(__name__)
from pymongo import MongoClient
bp = Blueprint('main', __name__, url_prefix='/')

client = MongoClient(
    'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbGatherHere

@bp.route('/')
def main():
    return render_template('main.html')

@bp.route('/movie', methods=['GET'])
def show_movie():
    show_movie = list(db.crawlingMovie.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_movie': show_movie})

@bp.route('/book', methods=['GET'])
def show_book():
    show_book = list(db.crawlingBook.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_book': show_book})

@bp.route('/album', methods=['GET'])
def show_album():
    show_album = list(db.crawlingalbum.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_album': show_album})

# if __name__ == '__main__':
#     bp.run('0.0.0.0', port=5000, debug=True)
