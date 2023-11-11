import requests as re
import time

def get_genre(release, artist, email, search_result=0, delay=1):
    """
    Gets the genre of a song/album if available in the MusicBrainz API.

    Parameters:
    release (str): Release/album of the song. Example: 'Bring Ya to the Brink'
    artist (str): Album/song artist. Example: 'Cyndi Lauper'
    email (str): Email of user for the User-Agent.
    search_result (int): The nth search result to use. Default first (0 index).
    delay (int): Delay to satisfy the API request rate limit. Default 1 second.


    Returns:
    top_genre (str): The genre with the most votes for a song's release/album
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'From': email
    }
    time.sleep(delay)

    test_search = re.get('https://musicbrainz.org/ws/2/release-group?query="' \
        + release + '"AND"' + artist +'"?inc=genres&fmt=json', headers=headers).json()
    
    # Return 'No genre' if no genre is available
    search_results = test_search['release-groups']
    if not search_result: return 'No genre'
    # Get the first search result by default 
    genres = search_results[search_result]['tags']
    # Sort the genres by number of votes
    genres.sort(key=lambda x: x['count'], reverse=True)
    # Get the top voted genre for the song's release/album
    top_genre = genres[0]
    return top_genre


