from discord import Embed
from musiclib.Playlist import Playlist
# Music Queue Manager
queues = {}
# The current track will only be removed from queue once we start playing the next track.

def get_queue(ID):
    if ID in queues:
        return queues[ID]
    else:
        return None
        print("playlist doesn't exist")

def enqueue(ID, track, pos=None):
    if ID in queues:
        queues[ID].add_track(track, pos)  # Add track to our current queue (Playlist object)
    else:
        queues[ID] = Playlist(ID)   # Create a new Playlist as our queue
        queues[ID].add_track(track, pos)

def dequeue(ID, pos = 0):
    if not ID in queues:
        return -1

    popped = None
    if queues[ID].get_size() > pos:
        popped = queues[ID].remove_track(pos)
    else:
        print("TODO: the pos is out of range of the queue. add something here")

    if queues[ID].get_size() == 0: # If queue doesn't have anymore tracks after dequeuing, delete the PLaylist object
        remove_queue(ID)

    return popped


def print_queue(ID):
    if ID in queues:
        for name, playlist in queues:
            print(name)
    else:
        print(f"Queue for <{ID}> doesn't exist")
        return -1

def get_embed(ID):
    # Returns a nice embed for the queue, we can send this embed Object as a nice message in Discord
    embed = Embed(title="Music Queue", color=0xFFFFFF)
    if not ID in queues:
        embed.add_field(name="Empty Queue!", value="is a nerd")
    else:
        tracks = queues[ID].get_tracks()  # Get the list of tracks for this channel's queue
        currentTrack = tracks[0]    # Current track for a queue will always be the first track in the queue
        embed.add_field(name=f"Now On {'[Looping :D]' if queues[ID].is_looping() else ''}", value = f"`0.` {currentTrack.title} | `{currentTrack.duration//60}:{str(currentTrack.duration%60).zfill(2)}`", inline=False)

        if len(tracks) > 1:  # If queue has upcoming tracks
            upcoming_str_list = []
            # We list out the rest of the tracks starting from tracks[1] onwards.
            for i, track in enumerate(tracks[1:], start = 1):
                upcoming_str_list.append(f"`{i}.` {track.title} | `{track.duration//60}:{str(track.duration%60).zfill(2)}`")
        else:
            upcoming_str_list = ["No more songs!"]
        embed.add_field(name="Upcoming", value="\n".join(upcoming_str_list), inline=False)
    return embed


def remove_queue(id):
    if id in queues:
        del queues[id]
        print(f"Queue {id} destroyed")
