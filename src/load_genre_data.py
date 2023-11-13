""" 
Note the data output of this file is already provided in data/match_genres.json

This file will load genre data
     It creates a json file of data where each entry is a song
     he data has the artist name, song name, top 3 genres, and metadata filename for each song
     
Credits - Kai Lee
"""

import requests as re
from collections import defaultdict
import os
import tables
import json


"""
The function get_genre below loads the top n genres of a song given its artist name and song title
Test use is shown right after (commented out)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'From': 'placeholder'  # TODO: replace this with your MB email
}

# possible genres: https://musicbrainz.org/genres 
def get_genre(artist, song, top_genre_count=1):  
    """ 
    get_genre makes a MB query and return N most common genres for the song, N=top_genre_count 
    artist: string
    song: string 
    top_genre_count: the number of genres to return, in descending order from most to least common
    """
    mb_url = "https://musicbrainz.org/ws/2/release-group"
    
    params = {
        'query': f'artist:"{artist}" AND recording:"{song}""?inc=genres',
        'fmt': 'json',
    }

    response = re.get(mb_url, params=params)    # GET request

    if response.status_code != 200: 
        print(f"Error for query <{artist}, {song}>: {response.status_code}")
        return None
    
    data = response.json()
    genres = defaultdict(int)   # key: genre, value: number of votes (# labels applied) for that genre

    if not data['release-groups']:  # assert not empty
        print(f"No valid release groups for <{artist}, {song}> found")
        return None 

    for i in range(len(data['release-groups'])):    # scum
        if 'tags' in data['release-groups'][i] and data['release-groups'][i]['tags']:
            for tag in data['release-groups'][i]['tags']:
                genres[tag['name']] += tag['count']

    if not genres:  # assert not empty
        print(f"No valid tags for <{artist}, {song}> found, skipping")
        return None 

    # get N most upvoted genres
    sorted_genres = sorted(genres, key=genres.get, reverse=True)[:top_genre_count]  
    
    return sorted_genres


# test_release = 'cold weather'
# test_artist = 'glass beach'

# # returns 10 most upvoted genre labels for cold weather by glass beach
# print(get_genre(test_artist, test_release, 10)) 

"""
The function match_genres below loads the before mentioned data, and writes it to a .json file called match_genre.json stored in the data folder
"""

# NOTE: scraping rate is not currently handled. can add 1 sec wait or smth but use at own risk

def match_genres(directory, output_fp, backup='../data/backup.json', num_genres=3):
    """
    match_genres matches genres to each h5 file 
    directory: root directory containing all nested h5 files
    output_fp: filepath of output json file containing genre matching data
    backup: filepath of backup json file for intermediate writes (uncomment code under intermediary save to use)
    num_genres: number of genres to match to each song
    """
    json_data = []  # list of dicts that will be stored as json strings
    for root, dirs, files in os.walk(directory):   # recurse through directory
        backup_data = []
        for file in files:
            hdf5_path = os.path.join(root, file)
            data = tables.open_file(hdf5_path, mode='r')
            try:
                artist = data.root.metadata.songs.cols.artist_name[:][0].decode('utf-8')
                song = data.root.metadata.songs.cols.title[:][0].decode('utf-8')
                genres = get_genre(artist, song, num_genres)
                if genres:
                    match = { 'artist': artist, 'song': song, 'genres': genres, 'filename': file}
                    json_data.append(match)
                    backup_data.append(match)
                
                print(f"artist: {artist}\tsong: {song}\tgenres: {genres}\tfilename: {file}")
            except Exception as e:  # generic catch-all, stops code from terminating halfway
                print(f"Error parsing info for file {hdf5_path}: {e}")
                data.close()

            data.close()

        # intermediary save - data is uglier, but prevents total loss of progress if runtime error is encountered
        if backup_data:
            with open(backup, 'a') as file:
                json.dump(backup_data, file, indent=4)

    with open(output_fp, 'w') as file:
        json.dump(json_data, file, indent=4)
    
    print('finished')
    
# Example use for this project
# match_genres('../data/lmd_matched_h5/', '../data/match_genre.json')