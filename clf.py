#contains all classification routines

from audio import read_spectral_data_for_time


def single_key_experiment(window_size_ms, clf, train_time_sec):
	#loop until empty input is detected
	while True:
		#the key I will press
		key = raw_input('Label num:')
		if not key: break

		i = 0
		X = []
		y = []
		while i < train_time_sec:
			i += (window_size_ms / float(1000))
			freq_spect = read_spectral_data_for_time(windows_size_ms)
			X.append(freq_spect)
			y.append(key)

	clf.fit(X, y)


	while True:
		freq_spect = read_spectral_data_for_time(window_size_ms)
		_label = clf.predict([freq_spect])
		print 'Predicting class {}'.format(_label[0])


from sklearn.svm import LinearSVC
import sys
if __name__ == '__main__':
	window_size_ms = 500
	if len(sys.argv) > 1:
		window_size_ms = int(sys.argv[1])
	
	training_time = 30

	print "Training time for each key is {} seconds".format(training_time)
	single_key_experiment(window_size_ms, LinearSVC(), training_time)
