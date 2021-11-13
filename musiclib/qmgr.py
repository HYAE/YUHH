from discord import Embed
from musiclib.Playlist import Playlist
# Music Queue Manager
queues = {}
# The current track will only be removed from queue once we start playing the next track.

def create_playlist(ID, track):
    return Playlist(ID)

def get_playlist(ID):
    print(ID, queues)
    if ID in queues:
        return queues[ID]
    else:
        print("TODO: something wrong in qmgr get_playlist().")
    return None

def enqueue(ID, track, pos=None):
    if ID in queues:
        queues[ID].enqueue(track,pos)
    else:
        queues[ID] = create_playlist(ID,track)

def dequeue(ID, pos = 0):
    popped = None
    if ID in queues:
        if len(get_queue(ID)) > pos:
            popped = queues[ID].dequeue(pos)
        elif len(get_queue(ID)) == 0:
            remove_queue(ID)
        else:
            print("TODO: the pos is out of range of the queue. add something here")
    else:
        return -1
    return popped
    
def get_queue(id): #technically get_playlist now
    if id in queues:
        return queues[id].get_tracks()
    else:
        return None

def print_queue(id):
    if id in queues:
        for name, source in queues:
            print(name)
    else:
        return -1

def get_embed(id):
    # Returns a nice embed for the queue
    embed = Embed(title="Music Queue", color=0xFFFFFF)
    if not id in queues:
        embed.add_field(name="Empty Queue!", value="is a nerd",)
    else:
        queue = get_queue(id)
        embed.add_field(name="Now Playing", value = f"`0.` {queue.get_tracks()[0].title} | `{queue.get_tracks()[0].duration//60}:{str(queue.get_tracks()[0].duration%60).zfill(2)}`", inline=False)

        if len(queue) > 1:  # If queue has upcoming tracks
            upcoming_str_list = []
            for i, track in enumerate(queue.get_tracks()[1:], start = 1):
                upcoming_str_list.append(f"`{i}.` {track.title} | `{track.duration//60}:{str(track.duration%60).zfill(2)}`")
        else:
            upcoming_str_list = ["No more songs!"]
        embed.add_field(name="Upcoming", value="\n".join(upcoming_str_list), inline=False)

    return embed


def remove_queue(id):
    if id in queues:
        del queues[id]
