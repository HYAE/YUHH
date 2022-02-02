class Playlist():
    def __init__(self, ID):
        self.ID = ID
        self.looping = False
        self.tracks = []
        self.currentTrack = None

    def add_track(self, track, pos=None):
        if pos != None:
            self.tracks.insert(pos,track)
        else:
            self.tracks.append(track)

    def remove_track(self, pos = 0):
        return self.tracks.pop(pos)

    def toggle_looping(self):
        self.looping = not self.looping

    def stop_looping(self):
        self.looping = False

    def is_looping(self):
        return self.looping

    def get_tracks(self):
        return self.tracks

    def set_current_track(self, track):
        self.currentTrack = track

    def get_current_track(self):
        return self.currentTrack

    def get_size(self):
        return len(self.tracks)
