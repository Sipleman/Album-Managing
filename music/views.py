import json

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import form as f
import myutils

import datetime

from .Model import Singer
from .DBConnection import DB

db = DB()

def main_page(request):
    return render(request, 'mainpage.html')


def to_music_insert(request):
    singers = db.get_singers()
    return render(request, 'music_insert.html', {'singers': singers})


def music_insert_with_albums(request):
    singers = db.get_singers()
    if request.method == 'POST':
        albums = db.get_albums_by_singer(request.POST['dropdown1'])

        return render(request, 'music_insert2.html', {'singers': singers, 'albums': albums, 'current_name': request.POST['name'], 'current_size': request.POST['size'], 'current_duration': request.POST['duration']})


def to_music_insert2(request):
    db.get_albums_id_by_singer(request.POST['dropdown1'])


def music_edit(request):
    if request.method == "POST":
        song_form = f.SongForm(request.POST)

        song_id = request.POST["id"]

        if db.change_song(song_id, song_form):
            msg = "Song was successfully changed"
        else:
            msg = "Something bad happened"

        return render(request, "msg_page.html", {"msg": msg})
    else:
        track_id = request.GET["track_id"]
        song = db.get_song_by_id(track_id)

        data = {'name': song["name"], 'duration':song["duration"], 'price':song["price"], 'id':track_id}
        form = f.SongForm(initial=data)

    return render(request, "music_edit.html", {"song_form": form})
        

def music_edit2(request):
    albums = db.get_albums()
    songs = db.get_songs_by_album(request.POST['dropdown'])

    return render(request.G, 'music_edit2.html', {'albums': albums, 'songs': songs})


def music_edit3(request):

    albums = db.get_albums()
    songs = db.get_songs_by_album(request.POST['dropdown'])
    song = db.get_song_by_name(request.POST['songs'])
    return render(request, 'music_edit3.html', {'albums': albums, 'songs': songs, 'current_name': song.name,
                                                  'current_size': song.size, 'current_duration': song.duration,
                                                'current_id': song.idsong})


def music_remove(request):
    if request.method == 'POST':
        song_id = request.POST['track_id']
        if db.delete_song(song_id):
            msg = 'Song successfully removed'
        else:
            msg = ' Something bad happened'

        return render(request, "msg_page.html", {"msg": msg})




def music_remove2(request):
    db = DB()

    albums = db.get_albums()
    songs = db.get_songs_by_album(request.POST['dropdown'])

    return render(request, 'music_remove2.html', {'albums': albums, 'songs': songs})


def track_edit(request):
    db = DB()

    db.update_song(request.POST['name'], request.POST['size'], request.POST['duration'], request.POST['id'])
    return HttpResponseRedirect('/music/musiclist/')


def track_delete(request):
    if request.method == 'POST':
        db.delete_song(request.POST["songs"])
        tmp = tuple()

        tracks = db.get_songs()
        for i in range(0, len(tracks)):
            newsong = {"idsong": tracks[i].idsong, "id_album": tracks[i].id_album, "duration": tracks[i].duration,
                       "name": tracks[i].name, "size": tracks[i].size, "id_singer": tracks[i].id_singer}
            Singer.Singer.update_values(newsong, tracks[i].id_album, tracks[i].id_singer)
            tmp += (newsong,)

    return render(request, 'musiclist.html', {'tracks': tmp})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = f.NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/music/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = f.NameForm()

    return render(request, 'insert_new_song.html', {'form': form})
# Create your views here.


def music_list(request):
    db = DB()
    tracks = db.get_songs()
    for track in tracks:
        track["album"] = db.get_album_by_id(track.pop("album_id"))["name"]
        track["author"] = db.get_singer_by_id(track.pop("author_id"))["name"]
    tmp = tuple()
    # t = {"idsong": tracks[0].idsong}
    # tmp+=(t,)

    return render(request, 'musiclist.html', {'tracks': tracks})


def albums_select(request):
    if request.method == "GET":
        albums = db.get_albums()

        for album in albums:
            album["author"] = db.get_singer_by_id(album["id_author"])["name"]
            album["price"] = db.get_album_price(album["name"])
            album["id"] = album.pop("_id")
        return render(request, "albums_select.html", {"albums": albums})


def album_overview(request, album_id):
    if request.method == "GET":
        album = db.get_album_by_id(album_id)
        album["author"] = db.get_singer_by_id(album["id_author"])["name"]
        tracks = album["songs"]
        for track in tracks:
            track["id"] = track["_id"]

    return render(request, 'album_overview.html', {"tracks": tracks, "album": album})


def to_music_search(request, type=""):
    db = DB()
    msg = {}
    msg['type'] = type

    if request.method == "POST":
        if type == "price":
            equation = request.POST["types"]
            msg['count'] = db.count_of_songs_with_price(request.POST["value"], equation)

        if type == "duration":
            equation = request.POST["types"]
            msg['count'] = db.count_of_songs_with_duration(request.POST["value"], equation)
    else:
        if type == "price":
            msg['msg'] = 'Enter price'
        if type == "duration":
            msg['msg'] = 'Enter duration'
    return render(request, 'to_search.html', {"msg": msg})


def music_search(request, type=""):
    db = DB()
    msg = {}
    if type != "":
        if type == "price":
            price = request.POST["value"]
            types = request.POST["types"]
            songs = db.count_of_songs_with_price(price, types)
            return render(request, "musiclist.html", {"tracks": songs})
        if type == "duration":
            price = request.POST["value"]
            types = request.POST["types"]
            songs = db.count_of_songs_with_duration(price, types)
            return render(request, "musiclist.html", {"tracks": songs})

    if type == "price":
        msg['msg'] = 'Enter price'
        msg['type'] = type
        return render(request, 'to_search.html', {"msg": msg})
    if type == "duration":
        msg['msg'] = 'Enter duration'
        msg['type'] = type
        return render(request, 'to_search.html', {"msg": msg})

        # if request.method == 'POST':
    #     tracks = db.get_songs_by_diapason(request.POST['value'], request.POST['value2'])
    #
    #     tmp = tuple()
    #     for i in range(0, len(tracks)):
    #         newsong = {"idsong": tracks[i].idsong, "id_album": tracks[i].id_album, "duration": tracks[i].duration,
    #                    "name": tracks[i].name, "size": tracks[i].size, "id_singer": tracks[i].id_singer}
    #         Singer.Singer.update_values(newsong, tracks[i].id_album, tracks[i].id_singer)
    #         tmp += (newsong,)

        return render(request, 'musicsearch.html', {'tracks': tmp, 'value': request.POST['value'],
                                                 'value2': request.POST['value2']})

def thanks(request):
    form = f.NameForm()
    return render(request, 'music_edit.html', {'form': form})


def add_track(request):
    if request.method == 'POST':
        form = request.POST
        print db.add_track(form['name'], form['duration'], form['price'], request.POST['album'])
        return HttpResponseRedirect('/music/musiclist/')
    else:
        album_id = request.POST["album"]
        data = {"id": album_id}
        form = f.SongForm(initial=data)

    return render(request, 'musiclist.html', {'song_form': form})


def add_new_song(request):
    if request.method == 'POST':
        singer_id = request.POST['the_post']
        albums = db.get_albums_by_singer_id(singer_id)
        response_data = {}
        response_data['result'] = 'Require success'
        response_data['the_post'] = albums

        return HttpResponse(
            myutils.JSONEncoder().encode(response_data),
            content_type="application/json"
        )
    else:
        db = DB()
        authors = db.get_singers()
        for author in authors:
            author["id"] = author.pop("_id")
        form = f.SongForm()
        return render(request, 'insert_new_song.html', {'authors': authors, "song_form": form})


def boolean_mode(request):
    if request.method == 'POST':
        db = DB()

        table = db.boolean_search_by_phrase(request.POST["value_bool"])

        return render(request, 'musicsearch.html', {'tracks': table})


def async_request(request):
    if request.method == 'POST':
        singer_id = request.POST['the_post']
        db = DB()
        albums = db.get_albums_by_singer_id(singer_id)
        response_data = {}
        response_data['result'] = 'Require success'
        response_data['the_post'] = albums

        return HttpResponse(
            myutils.JSONEncoder().encode(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )