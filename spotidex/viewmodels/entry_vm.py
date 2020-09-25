from spotidex.models.spotifyAuth import SpotifyAuth


class EntryVM:
    
    def __init__(self):
        self.__callback = SpotifyAuth.get_instance().currently_playing
        self.current = self.__callback()
        
    
    
    
    def refresh(self, write_func, close_pipe):
        
        new_track = self.__callback()
        if self.current != new_track:
            self.current = new_track
            write_func(self.current)
        
        close_pipe()
        
        
        