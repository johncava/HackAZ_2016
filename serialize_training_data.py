from audio import read_spectral_data_for_time
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import sys
def get_training_data(window_size_ms, train_time_sec=30):
	#loop until empty input is detected
	X = []
	y = []

	print "Training time for each key is {} seconds".format(train_time_sec)
	i = 0
	while True:
		s = raw_input('Press <enter> to begin training key {} or q-<enter> to quit'.format(i))
		if s: break

		j = 0
		while j < train_time_sec:
			j += (window_size_ms / float(1000))
			freq_spect = read_spectral_data_for_time(window_size_ms)
			X.append(freq_spect)
			y.append([i])

		#increment key counter
		i += 1

	mb = MultiLabelBinarizer()
	y = mb.fit_transform(y)

	X = np.asarray(X)
	y = np.asarray(y)
	return X, y

import time, threading, sys, pickle
if __name__ == '__main__':

	if len(sys.argv) < 2:
		print 'Usage: <script-name> <output-filename>'
		sys.exit()

	outfile = sys.argv[1]
	window_size_ms = 75
	kwargs = {}
	if len(sys.argv) > 1:
		window_size_ms = int(sys.argv[1])
	if len(sys.argv) > 2:
		kwargs['train_time_sec'] = int(sys.argv[2])

	X, y = get_training_data(window_size_ms, **kwargs)

	with open(outfile, 'wb') as f:
		pickle.dump((X, y), f)

	print 'Dumped (X, y) to {}'.format(outfile)

