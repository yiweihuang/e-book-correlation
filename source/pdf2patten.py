#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

# python pdf2patten.py book/computernetwork-1.pdf 27 book/computernetwork-1.en.text
# python pdf2patten.py book/computernetwork-2.pdf 33 book/computernetwork-2.en.text
# python pdf2patten.py book/computernetwork-3.pdf 4 book/computernetwork-3.en.text
if len(sys.argv) < 4:
    print('Usage: python pdf2patten.py book/computernetwork-1.pdf 27 book/computernetwork.en.text')
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
        if pageNumber >= 4:
            interpreter.process_page(page)
            data =  retstr.getvalue()
    data = re.sub(r'[^\w\s]', '', data)
    os.remove(sys.argv[3]) if os.path.exists(sys.argv[3]) else None
    with open(sys.argv[3], 'w') as f:
        f.write(data)

if __name__ == '__main__':
    pdfparser(sys.argv[1])
