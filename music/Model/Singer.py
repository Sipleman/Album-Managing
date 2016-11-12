from music.DBConnection import DB


class Singer(object):
    def __init__(self):
        self.name = ''
        self.lastName = ''
        self.birthday_date = ''

    @staticmethod
    def update_values(song, id_album, id_signer):
        db = DB()
        album = db.get_album_by_id(id_album)
        singer = db.get_singer_by_id(id_signer)
        song['year'] = album.year
        song['genre'] = album.genre
        song['album_name'] = album.album_name
        song['singer'] = singer.name
        return song

