from lib.Song import Song
import ast

class Queue:

    def __init__(self, cache): 
        self.cache = cache
        self.cache.set('queue', [])
        self.cache.set('history', [])

    def addSong(self, song):
        queue = self.instantiate_queue()
        index = None
        for song, i in enumerate(queue):
            if not song['explicit']:
                index = i
                break

        if index is None:
            index = len(queue)

        queue[index] = song.to_dict()

        self.sortSongs(queue)
        self.cache.set('queue', queue)

    def addImplicit(self, queue, history):
        song_seeds = []

        for song in history:
            if song['explicit']:
                song_seeds.append(song)
        
        if len(song_seeds) < 5:
            for song in history:
                if song['explicit']:
                    song_seeds.append(song)

        if len(song_seeds) > 5:
            song_seeds = song_seeds[:5]
        
        num = 5 - len(queue)
        new_songs = get_implicit_songs(song_seeds, num)
        queue.extend(new_songs)

    def getSong(self):
        queue = self.instantiate_queue()
        song_data = queue.pop(0)

        history = self.instantiate_history()
        history.append(song_data)

        if len(queue) < 5:
            self.addImplicit(queue, history)
        
        self.ageSongs(queue)
        self.calculateScore(queue)
        self.sortSongs(queue)

        self.cache.set('queue', queue)
        self.cache.set('history', history)

        keys = ['name', 'track_id', 'artist', 'album_uri', 'album_name', 'duration', 'explicit']
        args = [song_data[key] for key in keys]
        return Song(*args)

    def sortSongs(self, queue):
        queue.sort(key = lambda x: x['score'])

    def calculateScore(self, queue):
        for song in queue:
            if song['explicit']:
                song['score'] = song['age']**1.5 + song['upvotes'] - song['downvotes']
            else:
                song['score'] = 0
        
    def ageSongs(self, queue):
        for song in queue:
            if song['explicit']:
                song['age'] += 1

    def instantiate_queue(self):
        serialized_queue = self.cache.get('queue')
        queue = ast.literal_eval(serialized_queue.decode('utf-8'))
        return queue

    def instantiate_history(self):
        serialized_history = self.cache.get('history')
        history = ast.literal_eval(serialized_history.decode('utf-8'))
        return history

    def serialize(self):
        return self.instantiate_queue()
        
