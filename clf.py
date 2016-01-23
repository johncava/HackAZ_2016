#contains all classification routines

from audio import read_spectral_data_for_time


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

import numpy as np

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

	while True:
		freq_spect = read_spectral_data_for_time(window_size_ms)
		_label = clf.predict([freq_spect])
		print 'Predicting classes {}'.format(mb.inverse_transform(_label)[0])


from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
import sys
if __name__ == '__main__':
	window_size_ms = 500
	training_time = 30
	n_keys = 3
	if len(sys.argv) > 1:
		window_size_ms = int(sys.argv[1])
	if len(sys.argv) > 2:
		training_time = int(sys.argv[2])
	if len(sys.argv) > 3:
		n_keys = int(sys.argv[3])


	clf = DecisionTreeClassifier()

	print "Training time for each key is {} seconds".format(training_time)
	#single_key_experiment(window_size_ms, LinearSVC(), training_time)
	multi_key_experiment(window_size_ms, OneVsRestClassifier(clf), training_time, n_keys=n_keys)


