from flask import Flask, request, url_for, session, redirect,render_template
import spotipy
import helper
import os
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import csv
import time
app = Flask(__name__)

app.secret_key = "nuishhe834j4r5"
app.config['SESSION_COOKIE_NAME'] = 'Sak Cookies'
TOKEN_INFO = "token_info"
@app.route('/')
def login():
    spotify_oauthorization = helper.create_spotify_oauth()
    authorize_url = spotify_oauthorization.get_authorize_url()
    return redirect(authorize_url)

@app.route('/redirect')
def redirectpage():
    spotify_oauthorization = helper.create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = spotify_oauthorization.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True))



@app.route('/getTracks')
def getTracks():
    try:
        token_info = helper.get_user_token(TOKEN_INFO)
    except:
        print("user not logged in")
        redirect(url_for("login", _external = False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    songs = []
    artists = []
    artist_name = []
    popularity = []
    counter = 0
    Length, Danceability, Acousticness, Energy, Instrumentalness, Liveness, Valence, Loudness, Speechiness, Tempo = ([] for i in range(10))
    for offsetamount in range(6):
        saved_tracks = sp.current_user_saved_tracks(limit=50, offset=offsetamount*50)['items']
    
        for i in range(len(saved_tracks)):
            songs.append(saved_tracks[i]['track']['name'])
            artists.append(saved_tracks[i]['track']['artists'][0]['name'])
            
            popularity.append(saved_tracks[i]['track']['popularity'])
    data = {
        'Song Name': songs,
        'Artist': artists,
        'Popularity': popularity,
        'Length': Length,
        'Danceability': Danceability,
        'Acousticness': Acousticness,
        'Energy': Energy,
        'Instrumentalness': Instrumentalness,
        'Liveness': Liveness,
        'Valence': Valence,
        'Loudness': Loudness,
        'Speechiness': Speechiness,
        'Tempo': Tempo
   
    }
    
    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data)
    
    # Export DataFrame to a CSV file
    df.to_excel('tracks.xlsx', index=False)
    return redirect(url_for("GetFeature", __external = False))
    #return render_template("GetTracks.html", songs_name = songs, artist = artists)
@app.route('/GetFeature')
def GetFeature():
    try:
        token_info = helper.get_user_token(TOKEN_INFO)
    except:
        print("user not logged in")
        redirect(url_for("login", _external = False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    Length, Danceability, Acousticness, Energy, Instrumentalness, Liveness, Valence, Loudness, Speechiness, Tempo = ([] for i in range(10))
    saved_tracks = sp.current_user_saved_tracks(limit=50, offset=0)['items']
    for i in range(len(saved_tracks)):
            # Make the API request
        test_track = saved_tracks[i]['track']['id']
            # print(test_track)
            # test_feature = None
            # delay = 1
            # time.sleep(delay)
            # while test_feature is None:
            #     try:
        print(i)
        test_feature = sp.audio_features(test_track)
                # except spotipy.exceptions.SpotifyException as e:
                    
                #     if e.http_status == 429:
                        
                #         # Rate limit exceeded, implement exponential backoff
                #         delay = 2 * delay  # Increase delay exponentially
                #         print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                        
                #         time.sleep(delay)
                #     else:
                #         # Other error occurred, handle it accordingly
                #         raise e

        for feature in range(len(test_feature)):
            Length.append((int(test_feature[feature]['duration_ms']) / 1000)/60)
            Danceability.append(test_feature[feature]['danceability'])
            Acousticness.append(test_feature[feature]['acousticness'])
            Energy.append(test_feature[feature]['energy'])
            Instrumentalness.append(test_feature[feature]['instrumentalness'])
            Liveness.append(test_feature[feature]['liveness'])
            Valence.append(test_feature[feature]['valence'])
            Loudness.append(test_feature[feature]['loudness'])
            Speechiness.append(test_feature[feature]['speechiness'])
            Tempo.append(test_feature[feature]['tempo'])    
    data = {
            'Length': Length,
            'Danceability':Danceability,
            'Acousticness':Acousticness,
            'Energy':Energy,
            'Instrumentalness':Instrumentalness,
            'Liveness':Liveness,
            'Valence':Valence,
            'Loudness':Loudness,
            'Speechiness':Speechiness,
            'Tempo':Tempo
        }
        
    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data)

    # Load the existing Excelfile
    existing_df = pd.read_excel('tracks.xlsx')

    # Concatenate the existing DataFrame and the new DataFrame
    updated_df = pd.concat([existing_df, df], axis=1)

    # Export the updated DataFrame to the Excel file

    return None




client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")