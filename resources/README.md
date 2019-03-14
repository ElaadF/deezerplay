# Deezerplay

1. Playlist data 2 datasets of 100 000 playlist
	- files : playlist2.txt, playlist1.txt (music\_1.npy, music\_2.npy for numpy version)
	- source : ["Word2vec applied to Recommendation: Hyperparameters Matter" by H. Caselles-Dupré, F. Lesaint and J. Royo-Letelier.](https://github.com/deezer/w2v_reco_hyperparameters_matter)
	- content : one playlist per line track\_deezerid, artist\_deezerid

2. Artist Metadata 
	- file : Artists.csv
	- source : [deezer api artist](https://developers.deezer.com/api/artist) for details on the fields 
	- file artist\_details\_spot.csv
	- source [spotify api artist](https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/) (+ deezerid) for details on the fields

2. Track data
	- file : Tracks.csv
 	- source : [deezer api artist](https://developers.deezer.com/api/track) for details on the fields
 	- file track\_details\_spot.csv
	- source [spotify api audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/) (+ deezerid) for details on the fields
