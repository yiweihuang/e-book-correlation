import sys
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

if len(sys.argv) < 3:
    print('Usage: python pdf2patten.py book/computernetwork.pdf book/computernetwork.en.text')
    sys.exit()

def pdfparser(data):

    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        if pageNumber >= 27:
            interpreter.process_page(page)
            data =  retstr.getvalue()
    data = re.sub(r'[^\w\s]', '', data)
    os.remove(sys.argv[2]) if os.path.exists(sys.argv[2]) else None
    with open(sys.argv[2], 'w') as f:
        f.write(data)

if __name__ == '__main__':
    pdfparser(sys.argv[1])

# python pdf2patten.py cn_slides/week1_en.pdf week1.en.text
