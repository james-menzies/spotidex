from spotidex.models.spotifyAuth import SpotifyAuth

auth = SpotifyAuth()

auth.establish_connection()

refresh = auth.currently_playing

song_info = refresh().information
print("basic info")
for item in song_info['basic_info'].items():
    print(item)

print("-------------")

for item in song_info['classical_info'].items():
    print(item)
    
print("------------")