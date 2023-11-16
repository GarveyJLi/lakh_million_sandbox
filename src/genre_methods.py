import requests as re
import time
import pretty_midi

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


def feature(id, file):
    """
    Extracts features from a PrettyMidi object created from a midi file

    Parameters:
    id (str): Song id
    file (str): Midi filepath

    Output:
    sd (dict): Song dictionary containing midi features

    """

    sd = {}
    spm = pretty_midi.PrettyMIDI(file)
    sd['song_id'] = id
    sd['instruments'] = [{'program_number': i.program, 
                          'is_drum': i.is_drum, 
                          'program_name': i.name} 
                          for i in spm.instruments]
    sd['key_changes'] = [{'key_number': k.key_number, 
                          'time': k.time} 
                          for k in spm.key_signature_changes]
    
    # Formats time signature changes as (time signature, tick)
    sd['time_signature_changes'] = [{'time_signature': str(ts.numerator) + "/" + \
                                        str(ts.denominator), 
                                    'time': ts.time
                                    } for ts in spm.time_signature_changes]
    sd['lyrics'] = [{'text': l.text, 
                     'time': l.time}
                        for l in spm.lyrics]
    
    sd['text_events'] = [{'text': l.text, 
                     'time': l.time}
                        for l in spm.text_events]
    
    # First array is when the tempo changes, second array is what it changes to 
    tc = spm.get_tempo_changes()
    # Dictionary of tempo changes and when they occur {time: tempo}
    sd['tempo_changes'] = dict(zip(tc[0], tc[1]))

    # Best tempo estimate from estimate_tempi(). FLoat
    sd['tempo'] = spm.estimate_tempo()
    # All beats in the song
    sd['beats'] = spm.get_beats()
    # When the beats start
    sd['beat_start'] = spm.estimate_beat_start()
    # Downbeat location in seconds
    sd['downbeats'] = spm.get_downbeats()
    # Note beginnings
    sd['onsets'] = spm.get_onsets()
    # Histogram of pitches in the song
    sd['pitch_class_histogram'] = spm.get_pitch_class_histogram()
    # Periodic form of the song
    sd['synthesis'] = spm.synthesize()
    return sd


