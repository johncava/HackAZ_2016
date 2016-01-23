'''
Created on Jan 23, 2016

@author: connor
'''
from Tkinter import Tk, Frame, Canvas, Button, BOTH

class ReaderDisplay(Canvas):
    NUMBER_OF_LINES = 6
    LINE_SPACING = 10 # pixels
    
    def __init__(self, parent):
        Canvas.__init__(self, parent, bg="#FFFFFF")
        for i in xrange(ReaderDisplay.NUMBER_OF_LINES):
            y = (i + 1.5) * ReaderDisplay.LINE_SPACING
            self.create_line(0, y, self['width'], y)
        

class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.parent.title("Music Reader")
        self.pack(fill=BOTH, expand=1)
        
        reader_display = ReaderDisplay(self)
        reader_display.grid(columnspan=4)
        
        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.grid(row=3, column=5, rowspan=1, columnspan=1)

def main():
    root = Tk()
    root.geometry("800x800+250+50")
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()