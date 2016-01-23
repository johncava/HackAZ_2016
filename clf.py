#contains all classification routines

from audio import read_spectral_data_for_time
from multiprocessing import Queue


def single_key_experiment(window_size_ms, clf, train_time_sec):
	#loop until empty input is detected
	X = []
	y = []
	while True:
		#the key I will press
		key = raw_input('Label num:')
		if not key: break

		i = 0
		while i < train_time_sec:
			i += (window_size_ms / float(1000))
			freq_spect = read_spectral_data_for_time(window_size_ms)
			X.append(freq_spect)
			y.append(key)

	clf.fit(X, y)


	while True:
		freq_spect = read_spectral_data_for_time(window_size_ms)
		_label = clf.predict([freq_spect])
		print 'Predicting class {}'.format(_label[0])


from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
import sys

import numpy as np

note_buffer = Queue()
clf = DecisionTreeClassifier()

def multi_key_experiment(window_size_ms, clf, train_time_sec, n_keys=3):
	#loop until empty input is detected
	X = []
	y = []
	labels = [(i,) for i in range(n_keys+1)]


	mb = MultiLabelBinarizer()
	labels = mb.fit_transform(labels)

	for label_num, label in enumerate(labels):
		raw_input('Press <enter> to begin training key {}'.format(label_num))
		i = 0
		while i < train_time_sec:
			i += (window_size_ms / float(1000))
			freq_spect = read_spectral_data_for_time(window_size_ms)
			X.append(freq_spect)
			y.append(label)

	X = np.asarray(X)
	y = np.asarray(y)
	clf.fit(X, y)
	
	return mb

window_size_ms = 500
training_time = 30
n_keys = 3

def listen(mb):
	while True:
		freq_spect = read_spectral_data_for_time(window_size_ms)
		_label = clf.predict([freq_spect])
		current_notes = mb.inverse_transform(_label)[0]
		note_buffer.put(current_notes)
		print str(current_notes)

def train():
	return multi_key_experiment(window_size_ms, OneVsRestClassifier(clf), training_time, n_keys=n_keys)

def main():
	if len(sys.argv) > 1:
		window_size_ms = int(sys.argv[1])
	if len(sys.argv) > 2:
		training_time = int(sys.argv[2])
	if len(sys.argv) > 3:
		n_keys = int(sys.argv[3])


	print "Training time for each key is {} seconds".format(training_time)
	#single_key_experiment(window_size_ms, LinearSVC(), training_time)
	train()

if __name__ == '__main__':
	main()
