from spotidex.models.spotifyAuth import SpotifyAuth

auth = SpotifyAuth()

auth.establish_connection()

refresh = auth.currently_playing

song_info = refresh().information


for item, value in song_info.items():

    print(item)
    print("----------")
    for attr in song_info[item].items():
        print(attr)