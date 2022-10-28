from pymongo import MongoClient
url = 'mongodb+srv://faulty:qwer1234@cluster0.qnaw7kn.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url)
db = client.dbGatherHere


db.crawlingAlbum.insert_many(list(db.crawlingalbum.find({},{"_id":False})))