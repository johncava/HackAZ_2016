#contains all classification routines
import numpy as np
from audio import read_spectral_data_for_time, read_temporal_spectral_data_for_time
import multiprocessing
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import sys, Queue


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

note_buffer = multiprocessing.Queue()

def listen(clf, mb, window_size_ms):
	while True:
		freq_spect = read_spectral_data_for_time(window_size_ms)
		_label = clf.predict([freq_spect])
		current_notes = mb.inverse_transform(_label)[0]
		for note in current_notes:
			note_buffer.put(note)
		print str(current_notes)

import matplotlib.pyplot as plt
import threading
import time
def plot_worker():
	PLOT_REFRESH = 0.5 #500 ms.

	while True:
		time.sleep(PLOT_REFRESH)
		if not sig_plot.plot_buffer.empty():
			(t, freq) = sig_plot.plot_buffer.get()

			#empty queue
			while not sig_plot.plot_buffer.empty():
				sig_plot.plot_buffer.get()

			plt.clf()
			plt.subplot(211)
			plt.plot(t)
			plt.subplot(212)
			plt.plot(freq)
			plt.draw()
			

class SignalPlot(object):
	def __init__(self):
		plt.ion()
		plt.show(block=False)
		self.plot_buffer = Queue.LifoQueue()
		plot_helper = threading.Thread(target=plot_worker)
		plot_helper.start()

sig_plot = SignalPlot()

def listen_single(clf, mb, window_size_ms):
	time_domain, freq_spect = read_temporal_spectral_data_for_time(window_size_ms)

	# TODO TEMP CMT sig_plot.update(time_domain, freq_spect)
	_label = clf.predict([freq_spect])
	current_notes = mb.inverse_transform(_label)[0]
	return current_notes

		
"""
INPUT:
window_size_ms - the sampling window size in ms
train_time_sec - the number of seconds spent on training each key
clf - The classifier which to train (Optional)
n_keys - The number of keys to train.

OUTPUT:
The trained classifier and the MultiLabelBinarizer

Routine Description:
Trains a classifier and returns the trained classifier and the multilabelbinarizer needed to convert the sparse labels to tuples
"""
def train(window_size_ms, train_time_sec=30, clf = OneVsRestClassifier(DecisionTreeClassifier()), n_keys=2):
	#loop until empty input is detected
	X = []
	y = []
	labels = [(i,) for i in range(n_keys+1)]

	mb = MultiLabelBinarizer()
	labels = mb.fit_transform(labels)

	print "Training time for each key is {} seconds".format(train_time_sec)
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
	return (clf, mb)

import time, threading
if __name__ == '__main__':
	window_size_ms = 75
	kwargs = {}
	if len(sys.argv) > 1:
		window_size_ms = int(sys.argv[1])
	if len(sys.argv) > 2:
		kwargs['train_time_sec'] = int(sys.argv[2])
	if len(sys.argv) > 3:
		kwargs['n_keys'] = int(sys.argv[3])

	clf, mp = train(window_size_ms, **kwargs)

def init_plots():
	while True:
		print listen_single(clf, mp, window_size_ms) 
