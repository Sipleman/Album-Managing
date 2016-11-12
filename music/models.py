# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Album(models.Model):
    id_album = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=45, blank=True, null=True)
    year = models.CharField(max_length=45, blank=True, null=True)
    numberofsongs = models.CharField(db_column='numberOfSongs', max_length=45, blank=True, null=True)  # Field name made lowercase.
    album_name = models.CharField(max_length=45, blank=True, null=True)
    id_singer = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Album'


class Singer(models.Model):
    id_singer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(db_column='lastName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    birthday = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Singer'


class Song(models.Model):
    idsong = models.AutoField(db_column='idSong', primary_key=True)  # Field name made lowercase.
    id_album = models.CharField(max_length=45, blank=True, null=True)
    duration = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    size = models.CharField(max_length=45, blank=True, null=True)
    id_singer = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Song'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
