# decluterfy
Tidy your old starred playlist and move songs to similar playlists you already own

## Starting the project

1. Download & Install Anaconda 4.2.0: [HERE](https://www.continuum.io/downloads#windows)
2. Create your virtual enviroment: `conda env create -f enviroment.yml`
3. Activate your new virtual env: `activate my_project_env`
4. Export oAuth env variables to your machine:
```
export SPOTIPY_CLIENT_ID="<you client id>"
export SPOTIPY_CLIENT_SECRET="<your client secret>"
export SPOTIPY_REDIRECT_URI="<your callback url>"
```
5. Run the file: `python main.py`
