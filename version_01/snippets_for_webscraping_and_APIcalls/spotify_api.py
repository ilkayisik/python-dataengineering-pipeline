#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:43:32 2022
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Initialize SpotiPy with user credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
                     client_id="",
                     client_secret=""))


# %% searching songs with queries:
# search for 'Lady Gaga', restricted to the first 10 results
results = sp.search(q="Lady Gaga", limit=10)

results.keys()
results["tracks"].keys()

# name of the first song returned by the API
results["tracks"]["items"][0]["name"]
# name of the artists
results["tracks"]["items"][0]["artists"]
# popularity of the track
results["tracks"]["items"][0]["popularity"]
# uniform resource identifier
results["tracks"]["items"][0]["uri"]

# %%
'''look for 10 songs by the Red Hot Chilli Peppers and store the `uri` of the
songs and their names.'''
# send request and store the response
red_hot = sp.search(q="Red hot chili peppers", limit=10)

# initialize empty lists that we will fill with information from our loop
list_of_uri, list_of_song_names = [], []

# iterate through the "items" (the songs)
# and append the "uri" and the "name" to the lists we created
for item in red_hot["tracks"]["items"]:
    print(item)
    list_of_uri.append(item["uri"])
    list_of_song_names.append(item["name"])

# print results
print(list_of_uri)
print(list_of_song_names)
# %% Searching multiple artists
artists = ["Red hot chili peppers", "SCARR", "Whitney Houston"]

results = []
for artist in artists:
    results.append(sp.search(q=artist, limit=10))


song_names = []
for result in results:
    for item in result["tracks"]["items"]:
        song_names.append(item["name"])

# %% PLAYLISTS
my_playlist = sp.user_playlist_tracks(user="spotify",
                                      playlist_id="spotify:playlist:0ce6Rmxf7QXroqa1wzjWY8")
my_playlist["items"][0]["track"]["uri"]
# %% AUDIO FEATURES
sp.audio_features("spotify:track:6Sy9BUbgFse0n0LPA5lwy5")

list_of_songs = []


def song_features(human_song_title):
    # search for the song title you enter into the function, limited to the first 2 results
    results = sp.search(q=human_song_title, limit=10)['tracks']['items']
    # create a loop, so we only select the parts of the json we need
    for i in results:
        # empty dictionary to be filled with the information below
        track_dict = {}
        # add the key artist and a corresponding value to the dictionary
        track_dict['Artist'] = i['artists'][0]['name']
        # add the key title and the corresponding value to the dictionary
        track_dict['Title'] = i['name']
        # add the key album and the corresponding value to the dictionary
        track_dict['Album'] = i['album']['name']
        # add the key audio description and the corresponding value to the dictionary
        track_dict['Audio Description'] = sp.audio_features(i['id'])
        # add the dictionary to the list list_of_songs
        list_of_songs.append(track_dict)
    # output list_of_songs
    return list_of_songs


# call the function with a song to test
song_features("Under the Bridge")

# make a dataframe from the list of songs created in the function above
df = pd.DataFrame(list_of_songs)

# quick function we can use to select only the 1st item
# this can also be done simply with [0], but we wanted to show you how you can incorporate a custom function into your work


def first_value(x):
    return x[0]


# making a DataFrame from the audio features of the songs in list_of_songs
df_audio_features = pd.json_normalize(df['Audio Description'].apply(first_value))

# merge the expanded audio features with the original DataFrame
df_audio_features = pd.merge(df, df_audio_features, left_index=True, right_index=True)

# drop the old ugly column where all the audio features are clumped together
df_audio_features.drop('Audio Description', axis=1, inplace=True)
# %%
"""Collect a big dataframe of songs with their audio features
Start by looking for a playlist on spotify and copy its url.
Extract the audio features for each song on your playlist.
Now collect the link of many playlists and do the same for all of them.
Structure the information as a dataframe where each row is a song and the
columns are audio features.
"""

# your code here
list_of_playlists = ["https://open.spotify.com/playlist/2V2y4unZj2p4e5eSiY6dX1?si=b771a3f49b864b69&nd=1",
                     "https://open.spotify.com/playlist/5V9ro0ceJVGZbwfinEkTqW?si=211cd9682fc04a12"]
track_list = []
for i in list_of_playlists:
    individual_playlist = sp.user_playlist_tracks(user="spotify", playlist_id=i)['items']
    for j in individual_playlist:
        track_dict = {}
        track_dict['Artist'] = j['track']['artists'][0]['name']
        track_dict['Title'] = j['track']['name']
        track_dict['Album'] = j['track']['album']['name']
        track_dict['Audio Description'] = sp.audio_features(j['track']['id'])
        track_list.append(track_dict)

print(track_list)

playlist_df = pd.DataFrame(track_list)


def first_value(x):
    return x[0]


df_a_f = pd.json_normalize(playlist_df['Audio Description'].apply(first_value))
new_playlist_df = pd.merge(playlist_df, df_a_f, left_index=True, right_index=True)

new_playlist_df.drop('Audio Description', axis=1, inplace=True)
new_playlist_df
