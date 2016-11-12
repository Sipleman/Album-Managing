from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^albums_select', 'music.views.albums_select', name="albums_select"),
    url(r'^album_overview/(?P<album_id>.*)$', 'music.views.album_overview', name='album_overview'),
    # url(r'^change_song/', 'music.views.change_song', name="change_song"),

    url(r'^msg_page/', 'music.views.to_music_insert', name="insert_page"),
    url(r'^insert/async_request$', 'music.views.async_request', name="async_request"),

    url(r'^insert/$', 'music.views.add_new_song', name="insert"),
    url(r'^add_track/', 'music.views.add_track', name="insert_track"),

    url(r'^insert2/', 'music.views.music_insert_with_albums'),


    # url(r'^remove/', 'music.views.async', name="remove_page"),

    url(r'^add_track', 'music.views.add_track'),

    url(r'^remove/', 'music.views.music_remove'),
    url(r'^delete_track/', 'music.views.track_delete'),

    url(r'^search/(?P<type>.*)', 'music.views.to_music_search', name="search"),
    url(r'^edit/', 'music.views.music_edit', name="edit_page"),
    url(r'^edit2/', 'music.views.music_edit2'),
    url(r'^edit3/', 'music.views.music_edit3'),
    url(r'^edit_track/', 'music.views.track_edit'),
    url(r'^main', 'music.views.main_page', name="homepage"),
    url(r'^musiclist', 'music.views.music_list'),
    url(r'^to_music_search', 'music.views.to_music_search'),
    url(r'^music_search/(?P<type>.*)', 'music.views.music_search', name="musicsearch_page"),
    url(r'^add_track', 'music.views.add_track'),
    url(r'^boolean_search', 'music.views.boolean_mode'),

]