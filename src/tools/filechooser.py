from tkinter import Tk
from tkinter.filedialog import askopenfilename


class FileChooser:
    def __init__(self):
        self._tk = Tk()

    def find_file(self):
        self._tk.withdraw()
        return askopenfilename()
