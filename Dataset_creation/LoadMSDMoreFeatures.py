import pandas as pd 
import numpy as np 
import hdf5_utils as HDF5
import hdf5_getters as g
import glob
import itertools
import collections
import sys




def getData(starting_point):

	starting = starting_point*10000
	files = glob.glob('/mnt/snap/data/*/*/*/*.h5')

	file_one_round = files[starting:starting+10000]

	artist_hotness = []
	artist_ids = []
	artist_familarity = []
	artist_location = []
	artist_name = []
	song_hotness = []
	song_title = []
	year = []
	album_name = []



	for f in file_one_round:
	    h5 = HDF5.open_h5_file_read(f)
	    
	    songYear = g.get_year(h5)
	    if songYear < 1990:
	    	continue

	    artisthotness = g.get_artist_hotttnesss(h5)
	    artistids = g.get_artist_id(h5)
	    artistfamilarity = g.get_artist_familiarity(h5)
	    artistlocation = g.get_artist_location(h5)
	    artistname = g.get_artist_name(h5)
	    songhotness = g.get_song_hotttnesss(h5)
	    songtitle = g.get_title(h5)
	    songyear = g.get_year(h5)
	    albumname = g.get_release(h5)
	    
	    

	    artist_hotness.append(artisthotness)
	    artist_ids.append(artistids)
	    artist_familarity.append(artistfamilarity)
	    artist_location.append(artistlocation)
	    artist_name.append(artistname)
	    song_hotness.append(songhotness)
	    song_title.append(songtitle)
	    year.append(songyear)
	    album_name.append(albumname)

	    #print(count)
	    #count = count + 1
	    h5.close()


	#def createDictsFrom2DArray(dictionary, colName, featureList):
	#	for i in range(0,12):
	#		dictionary[colName+str(i)] = featureList[i]
		#i = 1
		#for t in itertools.izip_longest(*featureList):
		#	dictionary[colName+str(i)] = t
		#	i = i + 1
	#	return dictionary



	data = collections.OrderedDict()

	data['year'] = year
	data['artist_name'] = artist_name
	data['artist_id'] = artist_ids
	data['artist_hotness'] = artist_hotness
	data['artist_familarity'] = artist_familarity
	data['artist_location'] = artist_location
	data['song_title'] = song_title
	data['song_hotness'] = song_hotness
	data['album_name'] = album_name
	



	


	df=pd.DataFrame(data)
	print('before return ' + str(starting_point))

	return df
	

