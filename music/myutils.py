import json
from bson import ObjectId


def refactor_id_in_songs(songs):
    output_songs = []
    for song in songs:
        _id = song["album_id"]
        song["album_id"] = _id
        output_songs.append(song)
        print song

    print songs
    print output_songs
    return output_songs


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
