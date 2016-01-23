'''
Created on Jan 23, 2016

@author: connor
'''
from Tkinter import *
from threading import Timer
from math import ceil

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
        print "rendering staff..."
        
        self.delete("all")
        
        self.create_lines(self.LR_OFFSET, self.winfo_height()/2 - 50)
        # TODO TEMP
        if len(self.notes) == 0 or self.notes[len(self.notes) - 1].time % 3 == 0:
            self.notes.append(Note(Note.B3_VALUE, 0))
        
        for note in self.notes:
            center_x = round(int(self.WIDTH) - ((note.time + 0.5) * Note.NOTE_WIDTH * ReaderDisplay.NOTE_WIDTHS_PER_UPDATE))
            #TO DO RENAME PORTION OF THE CENTER_Y OFFSET AS A SCALE OFFSET
            center_y = 70 + (self.winfo_height()/2) - self.TOP_OFFSET + (5 + note.value - Note.B3_VALUE)  * Note.NOTE_WIDTH / 2
            
            self.create_line(center_x - Note.NOTE_WIDTH / 2, center_y - Note.NOTE_WIDTH / 2, center_x + Note.NOTE_WIDTH / 2 + 1, center_y + Note.NOTE_WIDTH / 2 + 1)
            self.create_line(center_x - Note.NOTE_WIDTH / 2, center_y + Note.NOTE_WIDTH / 2, center_x + Note.NOTE_WIDTH / 2 + 1, center_y - Note.NOTE_WIDTH / 2 - 1)

    def update_staff(self):
        for i in xrange(len(self.notes)):
            self.notes[i].time += 1
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