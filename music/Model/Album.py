
class Album(object):

    def __init__(self):
        self.id = ''
        self.genre = ''
        self.year = ''
        self.numberOfSongs = ''

    def set_parameters(self, id, genre, year, numb):
        self.id = id
        self.genre = genre
        self.year = year
        self.numberOfSongs = numb
