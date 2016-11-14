import MySQLdb as mdb
import xml.etree.ElementTree as ET

from bson import *
from pymongo import MongoClient

from .models import *
import sys


class DB(object):

    def __init__(self):
        # type: () -> object
        self.con = None
        self.openConnection = False
        self.connect()

        self.client = MongoClient()
        self.db = self.client.music_db

    def count_of_songs_with_price(self, price, equation):
        if equation == "gt":
            equation = ">"
        if equation == "lt":
            equation = "<"

        map_function = Code("function(){"
                   "    for(var i=0 in this.songs){"
                   "        if(this.songs[i].price" + equation + str(price) + "){"
                                                               "            emit(this.songs[i].price, 1);"
                                                               "            }"
                                                               "        }"
                                                               "    }")

        reduce_function = Code("function(key, values){"
                      "    var sum = 0;"
                      "    for( var i=0 in values){"
                      "        sum+=values[i];"
                      "        }"
                      "    return sum;"
                      "    }")
        result = self.db.album.inline_map_reduce(map_function, reduce_function, "myresult")
        total = 0
        print result
        for el in result['results']:
            total+=el['value']
        return total

    def count_of_songs_with_duration(self, duration, equation):
        if equation == "gt":
            equation = ">"
        if equation == "lt":
            equation = "<"

        map_function = Code("function(){"
                            "for(var i = 0 in this.songs){"
                            "duration = this.songs[i].duration.split(':');"
                            "equation = \"" + duration + "\".split(':');"
                               "if (duration[0]==equation[0]){"
                               "if (duration[1]" + equation + "equation[1])"
                               "emit(this.songs[i].duration, 1);"
                               "}"
                               "else{"
                               "if (duration[0]" + equation + "equation[0])"
                               "emit(this.songs[i].duration, 1);"
                               "}"
                               "}"
                               "}")

        reduce_function = Code("function(key, values){"
                               "var sum = 0;"
                               "for(var i=0 in values){"
                               "sum+=values[i];"
                               "}"
                               "return sum;"
                               "}")
        result = self.db.album.inline_map_reduce(map_function, reduce_function, "myresult")
        total = 0
        print result
        for el in result['results']:
            total += el['value']
        return total

    def get_album_price(self, album_name):
        value = list(self.db.album.aggregate([
                                    {"$match": {'name': album_name}},
                                    {"$unwind": '$songs'},
                                    {"$group": {'_id': '$songs._id', "price": {"$first": "$songs.price"}}},
                                    {"$group": {'_id': "album_price", "total": {"$sum": "$price"}}}
                                ]))[0]
        return value['total']

    def connect(self):
        try:
            self.con = mdb.connect('localhost', 'root', '(9)', 'musicdb')
            cur = self.con.cursor()
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

    def get_albums(self):
        return list(self.db.album.find({}))

    def get_singers(self):
        return list(self.db.author.find({}))

    def get_songs_by_album(self, album_id):
        with self.con:
            # cur = self.con.cursor(mdb.cursors.DictCursor)
            #
            # cur.execute("SELECT * FROM Song WHERE id_album = (SELECT id_album FROM Album WHERE album_name='" +
            #             album + "');")
            album = self.db.album.find({"_id": ObjectId(album_id)})
            return album[0]["songs"]
            res = Album.objects.get(album_name=album)
            result = Song.objects.filter(id_album=res.id_album)
            return result

    def get_song_by_name(self, song_name):
        # cur = self.con.cursor(mdb.cursors.DictCursor)
        # cur.execute("SELECT * FROM Song WHERE name = '" + name + "';")
        albums = self.db.album.find({})
        for album in albums:
            for song in album["songs"]:
                if song["name"] == song_name:
                    return song
        return {}

    def get_song_by_id(self, id):
        list_of_albums= list(self.db.album.find({},
                                 {"songs": {"$elemMatch": {"_id": ObjectId(id)}}}))
        for element in list_of_albums:
            if "songs" in element:
                return element["songs"][0]
        return None

    def change_song(self, song_id, form):

        return self.db.album.update({"songs._id": ObjectId(song_id)}, { "$set": {"songs.$.name": form['name'].value(),
                                                                     "songs.$.duration": form['duration'].value(),
                                                                     "songs.$.price": form['price'].value()}})

    def add_track(self, song_name, duration, price, id_album, id_singer=0):
        with self.con:
            song = {"_id": ObjectId(), "name": song_name, "album_id": ObjectId(id_album), "price": price,
                    "duration":duration, "author_id": ObjectId(id_singer)}
            return self.db.album.update({"_id": ObjectId(id_album)}, {"$addToSet": {"songs": song}})
            # return True
        return False

    def get_songs(self):
        with self.con:
            list_of_albums = self.db.album.find({}, {"songs":1})
            all_songs = []
            for list_of_song in list_of_albums:
                all_songs+=list_of_song["songs"]

            return all_songs

            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM Song")
            result = Song.objects.all()
            return result

    def get_album_by_id(self, id):
        with self.con:
            return self.db.album.find({"_id": ObjectId(id)})[0]
            cur = self.con.cursor()
            cur.execute("SELECT * FROM Album WHERE id_album='" + id + "'")
            result = Album.objects.get(id_album__exact=id)
            return result

    def get_singer_by_id(self, id):
        with self.con:
            return self.db.author.find({"_id": ObjectId(id)})[0]

            cur = self.con.cursor()
            cur.execute("SELECT * FROM Singer WHERE id_singer = '" + id + "'")
            result = Singer.objects.get(id_singer=id)
            return result


    def get_album_id_By_name(self, a_name):
        with self.con:
            return self.db.album.find({"name":a_name}, {"_id":1})[0]["_id"]
            cur = self.con.cursor()
            # cur.execute("SELECT id_album FROM Album WHERE album_name='" + name + "'")
            album = Album.objects.get(album_name=a_name)
            return album.id_album

    def get_singer_id_by_name(self, s_name):
        with self.con:
            return self.db.author.find({"_id": s_name}, {"_id":1})[0]

            cur = self.con.cursor()
            # cur.execute("SELECT * FROM Singer WHERE id_singer='" + name + "'")
            singer = Singer.objects.get(name=s_name)
            return singer.id_singer
            # return cur.fetchall()

    def get_albums_by_singer_id(self, id_singer):
        with self.con:
            return list(self.db.album.find({"id_author": ObjectId(id_singer)}))

            singerName = str(singerName)
            cur = self.con.cursor()
            cur.execute("SELECT id_singer FROM Singer WHERE name='" + singerName + "'")
            singer = Singer.objects.get(name=singerName)
            albums = Album.objects.filter(id_singer=singer.id_singer)
            # id_singer = cur.fetchall()
            # id_singer = id_singer[0][0]
            #
            # cur = self.con.cursor(mdb.cursors.DictCursor)
            #
            # cur.execute("SELECT DISTINCT alb.album_name FROM Album alb INNER JOIN ("
            #                           "(SELECT * FROM Song WHERE id_singer='" + str(id_singer) + "') " +
            #                         "AS s) ON alb.id_album = s.id_album; ")
            # al = cur.fetchall()
            return albums

    def get_songs_by_diapason(self, FROM, TO):
        with self.con:

            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM Song s INNER JOIN ((SELECT * FROM Album WHERE year>{0} AND year<{1})AS a) ON s.id_album=a.id_album".format(FROM, TO));
            albums = Album.objects.filter(year__gt=FROM, year__lt=TO)
            songs = tuple()

            if len(albums)>0:
                for album in albums:
                    songset = Song.objects.filter(id_album=album.id_album)
                    for element in songset:
                        songs += (element,)
            return songs


    def update_song(self, s_name, s_size, s_duration, s_id):
        with self.con:
            # cur = self.con.cursor()
            # query = "UPDATE Song SET name='{0}', size='{1}', duration='{2}' WHERE idSong='{3}'".format(name, size, duration, id)
            # cur.execute(query)
            s = Song.objects.get(idsong=s_id)
            s.name = s_name
            s.size = s_size
            s.duration = s_duration
            s.id = s_id
            s.save()
            # Song.objects.filter(idsong=s_id).update(name=s_name, size=s_size, duration=s_duration, idsong=s_id)

    #
    # def get_albums_id_by_singer(self, singerName):
    #     with self.con:
    #         cur = self.con.cursor()
    #         cur.execute("SELECT * FROM Album WHERE")
    #

    def get_count_of_song_gt(self, value):
        self.db.album.mapReduce(
            "function(){ for( var i:=0 in this.songs){ if(this.songs[i].price>}}"
        )

    def delete_song(self, song_id):
        with self.con:
            return self.db.album.update({"songs._id": ObjectId(song_id)}, { "$pull":
                                                                         { "songs": {"_id": ObjectId(song_id)}}})
            # cur = self.con.cursor()
            # cur.execute("DELETE FROM Song WHERE name='" + song_name + "';")
            Song.objects.get(name=song_name).delete()

    def boolean_search_by_phrase(self, value):
        with self.con:
            cur = self.con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM Song, Album WHERE MATCH (name, album_name, genre) "
                        "AGAINST ('+{0}*' IN BOOLEAN MODE);".format(value))
            return cur.fetchall()

    def kek(self):
        tree = ET.parse('data.xml')
        root = tree.getroot()
        with self.con:
            cur = self.con.cursor()
            for child in root:
                if child.tag == "Albums":
                    for album in child:
                        print album.attrib["album_name"]
                if child.tag == "Songs":
                    for song in child:
                        print song.attrib["name"]
                    for singer in child:
                        print singer.attrib["name"]

    def load_from_xml(self):
        tree = ET.parse('music/data.xml')
        root = tree.getroot()
        with self.con:
            cur = self.con.cursor()
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("SET AUTOCOMMIT = 0")
            cur.execute("START TRANSACTION")
            cur.execute("TRUNCATE Album")
            cur.execute("TRUNCATE Song")
            cur.execute("TRUNCATE Singer")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            cur.execute("COMMIT")
            cur.execute("SET AUTOCOMMIT = 1")
            for child in root:
                if child.tag == "Albums":
                    for album in child:
                        cur.execute(
                            "INSERT INTO Album (genre, year, numberOfSongs, album_name, id_singer) VALUES('{0}', '{1}',"
                            "'{2}', '{3}', '{4}');".format(album.attrib["genre"], album.attrib["year"], album.attrib["numberOfSongs"],
                                                     album.attrib["album_name"], album.attrib["id_singer"]))

                if child.tag == "Songs":
                    for song in child:
                        cur.execute(
                            "INSERT INTO Song (id_album, duration, name, size, id_singer) VALUES('{0}', '{1}',"
                            "'{2}', '{3}', '{4}');".format(song.attrib["id_album"], song.attrib["duration"],
                                                           song.attrib["name"],
                                                           song.attrib["size"], song.attrib["id_singer"]))
                if child.tag == "Singers":
                    for singer in child:
                        cur.execute("INSERT INTO Singer (name, lastName, birthday) "
                                    "VALUES('{0}', '{1}', '{2}');".format(singer.attrib["name"],
                                                                        singer.attrib["lastName"],
                                                                        singer.attrib["birthday"]))
db = DB()
# print db.get_songs_by_album("Destiny")
# print db.get_albums_by_singer("100 Wat Vipers")
# db.load_from_xml()

