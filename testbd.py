import bson
from pymongo import MongoClient

client = MongoClient()
db = client.music_db
price = "1"


def update_price(name):

    songs = db.album.find({"name": name})[0]["songs"]
    for song in songs:
        song['price'] = 1.29

    db.album.update({"name": name}, {"$set": {"songs": songs}})
    print db.album.find({"name": name})[0]

update_price("Second Helping")
