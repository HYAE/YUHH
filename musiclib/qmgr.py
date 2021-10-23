from discord import Embed
# Music Queue Manager
queues = {}
# The current track will only be removed from queue once we start playing the next track.

def enqueue(id, track):
    if id in queues:
        queues[id].append(track)
    else:
        queues[id] = [track]

def dequeue(id, pos = 0):
    if id in queues:
        if len(queues[id]) > pos:
            popped = queues[id].pop(0)
        if len(queues[id]) == 0:
            remove_queue(id)
    else:
        return -1
    return popped

def get_queue(id):
    if id in queues:
        return queues[id]
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
        embed.add_field(name="Now Playing", value = f"`0.` {queue[0].title} | `{queue[0].duration//60}:{str(queue[0].duration%60).zfill(2)}`", inline=False)

        if len(queue) > 1:  # If queue has upcoming tracks
            upcoming_str_list = []
            for i, track in enumerate(queue[1:], start = 1):
                upcoming_str_list.append(f"`{i}.` {track.title} | `{track.duration//60}:{str(track.duration%60).zfill(2)}`")
        else:
            upcoming_str_list = ["No more songs!"]
        embed.add_field(name="Upcoming", value="\n".join(upcoming_str_list), inline=False)

    return embed


def remove_queue(id):
    if id in queues:
        del queues[id]
