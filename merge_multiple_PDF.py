from PyPDF2 import PdfMerger
import os

#var=os.getcwd() for extracting from another folder

# Merge all PDF files in the current directory
merger = PdfMerger()
for item in os.listdir():  # Use the appropriate directory path
    if item.endswith('.pdf'):
        merger.append(item)

# Write the merged content to 'Final_pdf.pdf'
merger.write('Final_pdf.pdf')
merger.close()
#'b' appended to the mode opens the file in binary mode
#'r'-->read

#numera i documenti in ordine

''' alternativo merge
from PyPDF2 import PdfMerger

pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()
'''