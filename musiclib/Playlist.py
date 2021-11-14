

class Playlist():
    def __init__(self, ID):
        self.ID = ID
        self.looping = False
        self.tracks = []
        self.playing = False
        self.currentTrack = None

    def enqueue(self, track, pos=None):
        if pos:
            self.tracks.insert(pos,track)
        else:
            self.tracks.append(track)

    def dequeue(self, pos = 0):
        self.tracks.pop(pos)

    def toogle_looping(self):
        self.looping = not self.looping

    def stop_looping(self):
        self.looping = False

    def toggle_playing(self):
        self.playing = not self.playing

    def get_tracks(self):
        return self.tracks

    def set_current_track(self, track):
        self.currentTrack = track
        
    def get_current_track(self):
        return self.currentTrack
    
