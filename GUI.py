'''
Created on Jan 23, 2016

@author: connor
'''
from Tkinter import *
from clf import train, listen_single
import sys
from sklearn.multiclass import OneVsRestClassifier
import matplotlib.pyplot as plt

LOOP_INTERVAL = 10

class Note():
    B3_VALUE = 1   # the numerical value representing B in the 3rd octave (right below "middle C")
    NOTE_WIDTH = 15 # pixels

    def __init__(self, value, time=0):
        self.value = value
        self.time = time

class ReaderDisplay(Canvas):
    NOTE_WIDTHS_PER_UPDATE = 0.75    # the number of note widths to shift all the notes every UPDATE_INTERVAL
    UPDATE_INTERVAL = 100 # milliseconds
    STAFF_OFFSET = 15 # pixels; the number of pixels between the top staff line and the top of the canvas
    WIDTH = 1000
    HEIGHT = 400
    TOP_OFFSET = 50
    LR_OFFSET = 0
    MIN = 100
    T_STAFF_OFFSET = 150
    B_STAFF_OFFSET = 0

    def __init__(self, parent, clf, mb, note_sample_window_size):
        Canvas.__init__(self, parent, bg="#FFFFFF", width = self.WIDTH, height = self.HEIGHT)

        self.tclef = PhotoImage(file="./images/tclef.gif", master=self)
        self.bclef = PhotoImage(file="./images/bclef.gif", master=self)

        print self.tclef
        self.last_note_set = ()
        self.notes = []
        self.clf = clf
        self.mb = mb
        self.note_sample_window_size = note_sample_window_size


        self.render_staff()
        self.after(ReaderDisplay.UPDATE_INTERVAL, self.update_staff)

    def create_lines(self, LR_margin, top_margin):
        for i in xrange(5):
            y = i * Note.NOTE_WIDTH + ReaderDisplay.STAFF_OFFSET
            self.create_line(LR_margin, y + top_margin, self.winfo_width(), y + top_margin)


        self.create_image(0, self.winfo_height()/2 - self.T_STAFF_OFFSET, image=self.tclef, anchor=NW)
        self.create_image(10, self.winfo_height()/2 , image=self.bclef, anchor=NW)
        self.image = self.tclef
        self.image2 = self.bclef
        self.pack(fill=BOTH, expand=1)

    def render_staff(self):
        # TODO TEMP
        print "rendering staff..."

        self.delete("all")

        # TODO TEMP
        print self.winfo_width()

        self.create_lines(self.LR_OFFSET, self.winfo_height()/2 - self.T_STAFF_OFFSET)
        self.create_lines(self.LR_OFFSET, self.winfo_height()/2 + self.B_STAFF_OFFSET)
        # TODO TEMP
        #if len(self.notes) == 0 or self.notes[-1].time % 3 == 0:
        #    self.notes.append(Note(Note.B3_VALUE))

        for note in self.notes:
            center_x = round(int(self.WIDTH) - ((note.time + 0.5) * Note.NOTE_WIDTH * ReaderDisplay.NOTE_WIDTHS_PER_UPDATE))
            #TO DO RENAME PORTION OF THE CENTER_Y OFFSET AS A SCALE OFFSET
            center_y = 70 + (self.winfo_height()/2) - self.TOP_OFFSET + (5 + note.value - Note.B3_VALUE)  * Note.NOTE_WIDTH / 2

            self.create_line(center_x - Note.NOTE_WIDTH / 2, center_y - Note.NOTE_WIDTH / 2, center_x + Note.NOTE_WIDTH / 2 + 1, center_y + Note.NOTE_WIDTH / 2 + 1)
            self.create_line(center_x - Note.NOTE_WIDTH / 2, center_y + Note.NOTE_WIDTH / 2, center_x + Note.NOTE_WIDTH / 2 + 1, center_y - Note.NOTE_WIDTH / 2 - 1)

    def is_new_note(self, note_values):
        # notes containing 0 (the baseline) or empty are not new notes
        if len(note_values) == 0 or 0 in note_values:
            return False
        elif len(self.notes) == 0:
            return True

        # if this note's values are not a subset of previous set of notes, it's a new note
        for note_value in note_values:
            if not note_values in self.last_note_set:
                return True
        return False

    def is_note_continuation(self, note_values):
        # empty tuples represent no baseline, but undefined notes; these are usually notes
        # that are dropping off, especially from chords, so consider it a continuation
        if len(note_values) == 0:
            return True
        elif 0 in note_values:
            return False
        else:
            return not self.is_new_note(note_values)

    def update_staff(self):
        note_values = listen_single(self.clf, self.mb, self.note_sample_window_size)
        print note_values

        for note in self.notes:
            note.time += 1

        if self.is_new_note(note_values) and not self.is_note_continuation(note_values):
            for note_value in note_values:
                self.notes.append(Note(note_value))

        self.render_staff()

        self.last_note_set = note_values

        self.after(ReaderDisplay.UPDATE_INTERVAL, self.update_staff)


class MainWindow(Frame):
    def __init__(self, parent, clf, mb, note_sample_window_size):

        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Music Reader")
        self.pack(fill=BOTH, expand=1)

        reader_display = ReaderDisplay(self, clf, mb, note_sample_window_size)
        reader_display.pack(fill=BOTH, expand=1)

def main():
    note_sample_window_size = 75
    training_time = 10
    number_of_keys = 4

    if len(sys.argv) > 1:
        note_sample_window_size = int(sys.argv[1])
    if len(sys.argv) > 2:
        training_time = int(sys.argv[2])
    if len(sys.argv) > 3:
        number_of_keys = int(sys.argv[3])

    # first, run the training function
    (clf, mb) = train(note_sample_window_size, train_time_sec=training_time, n_keys=number_of_keys)

    root = Tk()
    root.geometry("1000x400")
    MainWindow(root, clf, mb, note_sample_window_size)
    menubar = Menu(root)
    menubar.add_command(label="Quit", command=root.quit)
    # display the menu
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
