import bencodepy
import hashlib
import os

class Torrent:
    def __init__(self, torrent_file):
        with open(torrent_file, 'rb') as f:
            self.meta = bencodepy.decode(f.read())
        self.announce = self.meta[b'announce'].decode('utf-8') # Tracker URL
        self.info = self.meta[b'info']
        self.info_hash = hashlib.sha1(bencodepy.encode(self.info)).digest() # SHA-1 hash of info dict
        self.piece_length = self.info[b'piece length']  # Size of each piece
        self.pieces = self.info[b'pieces'] # Concatenated SHA-1 hashes of pieces
        self.total_length = self._get_total_length()
        self.files = self._get_files()
        self.num_pieces = (self.total_length + self.piece_length - 1) // self.piece_length
        
    def _get_total_length(self):
        if b'files'in self.info: # Multi-file torrent
            return sum(file[b'length'] for file in self.info[b'files'])
        else:
            return self.info[b'length'] # Single-file torrent
        
    def _get_files(self):
        if b'files' in self.info:
            return [(file[b'path'][0].decode(), file[b'length']) for file in self.info[b'files']]
        else:
            return [(self.info[b'name'].decode(), self.info[b'length'])]
        

# torrent = Torrent('cosmos-laundromat.torrent')
# print('URL: ', torrent.announce, '/length: ', torrent.total_length, '/Pieces: ', torrent.num_pieces)