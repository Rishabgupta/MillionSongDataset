import pandas as pd 
import numpy as np 
import hdf5_utils as HDF5
import hdf5_getters as g
import glob
import itertools
import collections
import sys

def createDictsFrom1DArray(dictionary, colName, featureList):
		i = 1
		for t in itertools.izip_longest(*featureList):
			dictionary[colName+str(i)] = t
			i = i + 1
		return dictionary


def getData(starting_point):

	starting = starting_point*10000
	files = glob.glob('/mnt/snap/data/*/*/*/*.h5')

	file_one_round = files[starting:starting+10000]

	artist_ids = []

	song_beats_persecond = []
	song_duration = []
	song_end_fade_in = []
	song_start_fade_out = []
	song_key = []
	song_loudness = []

	song_segments_loudness_max = []
	song_segments_loudness_min = []
	song_segments_loudness_med = []

	song_segments_loudness_time_max = []
	song_segments_loudness_time_min = []
	song_segments_loudness_time_med = []

	song_mode = []
	song_sections_start = []
	song_pitches = []
	song_timbre = []
	song_tempo = []
	song_time_signature = []
	song_title = []
	artist_name = []
	year = []


	idx = np.triu_indices(12)

	#count = 1

	for f in file_one_round:
	    h5 = HDF5.open_h5_file_read(f)
	    
	    songYear = g.get_year(h5)
	    if songYear < 1990:
	    	continue

	    artist_id = g.get_artist_id(h5)
	    song_beat = (g.get_beats_start(h5)).tolist()
	    songDuration = g.get_duration(h5)
	    song_beat_persecond = float(len(song_beat))/songDuration

	    song_end_fadein = g.get_end_of_fade_in(h5)
	    song_start_fadeout = g.get_start_of_fade_out(h5)
	    songKey = g.get_key(h5)
	    songLoudness = g.get_loudness(h5)
	    
	    song_loudness_max = (g.get_segments_loudness_max(h5)) // 10
	    song_loudness_antilog = np.power(10, song_loudness_max)
	    song_segmentsLoudness_max = np.amax(song_loudness_antilog)
	    song_segmentsLoudness_min = np.amin(song_loudness_antilog)
	    song_segmentsLoudness_med = np.median(song_loudness_antilog)

	    song_segmentsLoudness_max_time = (g.get_segments_loudness_max_time(h5)).tolist()   
	    song_loudness_time = np.multiply(song_loudness_antilog, song_segmentsLoudness_max_time)
	    song_segmentsLoudnessTime_max = np.amax(song_loudness_time)
	    song_segmentsLoudnessTime_min = np.amin(song_loudness_time)
	    song_segmentsLoudnessTime_med = np.median(song_loudness_time)

	    songMode = g.get_mode(h5)
	    song_sectionsStart = (g.get_sections_start(h5)).tolist()
	    songPitches = g.get_segments_pitches(h5)
	    songPitches_cov = np.cov(songPitches, rowvar = False)
	    songPitches_mean = np.mean(songPitches, axis = 0)
	    #print(songPitches_cov.shape)
	    songTimbre = g.get_segments_timbre(h5)
	    songTimbre_cov = np.cov(songTimbre, rowvar = False)
	    songTimbre_mean = np.mean(songTimbre, axis = 0)
	    #print(songTimbre_cov.shape)
	    songTempo = g.get_tempo(h5)
	    songTime_signature = g.get_time_signature(h5)
	    songTitle = g.get_title(h5)
	    artistName = g.get_artist_name(h5)
	    

	    artist_ids.append(artist_id)

	    song_beats_persecond.append(song_beat_persecond)
	    song_duration.append(songDuration)
	    song_end_fade_in.append(song_end_fadein)
	    song_start_fade_out.append(song_start_fadeout)
	    song_key.append(songKey)
	    song_loudness.append(songLoudness)

	    song_segments_loudness_max.append(song_segmentsLoudness_max)
	    song_segments_loudness_min.append(song_segmentsLoudness_min)
	    song_segments_loudness_med.append(song_segmentsLoudness_med)

	    song_segments_loudness_time_max.append(song_segmentsLoudnessTime_max)
	    song_segments_loudness_time_min.append(song_segmentsLoudnessTime_min)
	    song_segments_loudness_time_med.append(song_segmentsLoudnessTime_med)

	    song_mode.append(songMode)
	    song_sections_start.append(song_sectionsStart)
	    pitches_mean_cov = (songPitches_cov[idx]).tolist()
	    pitches_mean_cov.extend((songPitches_mean).tolist())
	    song_pitches.append(pitches_mean_cov)
	    timbre_mean_cov = (songTimbre_cov[idx]).tolist()
	    timbre_mean_cov.extend((songTimbre_mean).tolist())
	    song_timbre.append(timbre_mean_cov)
	    song_tempo.append(songTempo)
	    song_time_signature.append(songTime_signature)
	    song_title.append(songTitle)
	    artist_name.append(artistName)
	    year.append(songYear)

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
	data['song_title'] = song_title
	data['song_beats_persecond'] = song_beats_persecond
	data['song_duration'] = song_duration
	data['song_end_fade_in'] = song_end_fade_in
	data['song_start_fade_out'] = song_start_fade_out
	data['song_key'] = song_key
	data['song_loudness'] = song_loudness

	data['song_loudness_max'] = song_segments_loudness_max
	data['song_loudness_min'] = song_segments_loudness_min
	data['song_loudness_med'] = song_segments_loudness_med

	data['song_loudness_time_max'] = song_segments_loudness_time_max
	data['song_loudness_time_min'] = song_segments_loudness_time_min
	data['song_loudness_time_med'] = song_segments_loudness_time_med

	data['song_mode'] = song_mode
	data['song_tempo'] = song_tempo
	data['song_time_signature'] = song_time_signature
	data = createDictsFrom1DArray(data, 'pitches', song_pitches)
	data = createDictsFrom1DArray(data, 'timbre', song_timbre)	

	data = createDictsFrom1DArray(data, 'sections_start', song_sections_start)

	


	df=pd.DataFrame(data)
	print('before return ' + str(starting_point))

	return df
	

