import pyPDF2

new_pdf = open('new.pdf','rb')
reading_pdf = pyPDF2.PdfFileReader(new_pdf)
print(reading_pdf.numPages)

pdf_page = reading_pdf.getPage(0)
print(pdf_page.exttractText())

new_pdf.close()