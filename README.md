# decluterfy
Tidy your old enourmous playlist and move songs to similar playlists you already own

## Starting the project

1. Download & Install [Anaconda 4.x.x][anaconda]: 
2. Create your virtual enviroment: `conda env-create -f enviroment.yml`
3. Activate your new virtual env: `activate decluterfy`
4. Export oAuth env variables to your machine from [developer page][dev-account]
```
export SPOTIPY_CLIENT_ID="<you client id>"
export SPOTIPY_CLIENT_SECRET="<your client secret>"
export SPOTIPY_REDIRECT_URI="<your callback url>"
```
5. Run the file: `python main.py`

[dev-account]: https://developer.spotify.com/my-applications/
[anaconda]: https://www.continuum.io/downloads
