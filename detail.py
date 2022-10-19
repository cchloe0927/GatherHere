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

@app.route('/detail/review', methods=["GET"])
def detail_movie_get():
    type = request.args.get('type') #if나중에
    id = request.args.get('id')
    print(type, id)
    detail_id = db.testmovie.find_one({'id': int(id)}, {'_id': False})
    print(detail_id)
    return jsonify({'detailID': detail_id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
