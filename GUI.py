'''
Created on Jan 23, 2016

@author: connor
'''
from Tkinter import Tk, Frame, Canvas, Button, BOTH
from clf import note_buffer, train, listen
from multiprocessing import Process

LOOP_INTERVAL = 10

class Note():
    B3_VALUE = 18   # the numerical value representing B in the 3rd octave (right below "middle C")
    NOTE_WIDTH = 10 # pixels
    
    def __init__(self, value, time=0):
        self.value = value
        self.time = time

class ReaderDisplay(Canvas):
    NOTE_WIDTHS_PER_UPDATE = 0.5    # the number of note widths to shift all the notes every UPDATE_INTERVAL
    UPDATE_INTERVAL = 100 # milliseconds
    STAFF_OFFSET = 15 # pixels; the number of pixels between the top staff line and the top of the canvas
    WIDTH = 1000
    HEIGHT = 400
    TOP_OFFSET = 130
    LR_OFFSET = 0
    
    def __init__(self, parent):
        Canvas.__init__(self, parent, bg="#FFFFFF", width = self.WIDTH, height = self.HEIGHT)
        self.notes = []
        self.render_staff()
        self.after(ReaderDisplay.UPDATE_INTERVAL, self.update_staff)
    
    def create_lines(self,LR_margin, top_margin):
        for i in xrange(5):
            y = i * Note.NOTE_WIDTH + ReaderDisplay.STAFF_OFFSET
            self.create_line(LR_margin, y + top_margin, self.winfo_width(), y + top_margin)
        
    def render_staff(self):
        # TODO TEMP
        #print "rendering staff..."
        
        self.delete("all")
        
        self.create_lines(self.LR_OFFSET, self.winfo_height()/2 - 50)
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
        
        # if this note's values are not a subset of previous set of notes, it's a new note
        note_values_index = -1
        latest_note_time = self.notes[-1]
        for latest_note in self.notes.reverse():
            if latest_note.time != latest_note_time:
                break
            elif note_values[note_values_index] == latest_note.value:
                note_values_index -= 1
                if note_values_index == -len(note_values):
                    break
        
        if note_values_index != -len(note_values):
            return True # note_values is _not_ a subset of the latest note values
    
    def is_note_continuation(self, note_values):
        # empty tuples represent no baseline, but undefined notes; these are usually notes
        # that are dropping off, especially from chords, so consider it a continuation
        if len(note_values) == 0:
            return True
        elif 0 in note_values:
            return False
        else:
            return not self.is_new_note()

    def update_staff(self):
        for i in xrange(len(self.notes)):
            self.notes[i].time += 1
            
        while not note_buffer.empty():
            note = note_buffer.get()
            if self.is_new_note(note):
                for note_value in note:
                    self.notes.append(Note(note_value))

        self.render_staff()
        
        self.after(ReaderDisplay.UPDATE_INTERVAL, self.update_staff)
        

class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.parent.title("Music Reader")
        self.pack(fill=BOTH, expand=1)
        
        reader_display = ReaderDisplay(self)
        reader_display.pack(fill=BOTH, expand=1)

def main():
    # first, run the training function
    mb = train()
    
    # then, start the listening in a separate process
    listen_process = Process(target=listen, args=(mb,))
    listen_process.start()
    
    root = Tk()
    root.geometry("1000x400")
    app = MainWindow(root)
    menubar = Menu(root)
    menubar.add_command(label="Quit", command=root.quit)
    # display the menu
    root.config(menu=menubar)
    root.mainloop()

if __name__ == '__main__':
    main()
