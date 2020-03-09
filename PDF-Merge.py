from PyPDF2 import PdfFileMerger
from tkinter import filedialog
import tkinter as tk
from os import chdir
from ntpath import dirname

application_window = tk.Tk()

filenames = filedialog.askopenfilenames(title="Select last file, press and hold Shift, select first file, click Open ")

application_window.destroy()

dirPath = dirname(filenames[0])
chdir(dirPath)

# pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']
merger = PdfFileMerger()

# for pdf in pdfs:
for pdf in filenames:
    merger.append(pdf)

merger.write("combined_pdf.pdf")
merger.close()