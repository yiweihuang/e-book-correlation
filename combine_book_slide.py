import sys
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

if len(sys.argv) < 4:
    print('Usage: python combine_book_slide.py book/computernetwork.pdf cn_slides/week1_en.pdf cn_slides/week1_zh.pdf combine_book_slide/week1.en.text')
    sys.exit()

def pdfparser(data, page_start, page_end):

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
        if pageNumber >= page_start and pageNumber <= page_end:
            interpreter.process_page(page)
            data =  retstr.getvalue()
    return data



if __name__ == '__main__':
    pdf_content = pdfparser(sys.argv[1], 27, 888)
    slide_content_en = pdfparser(sys.argv[2], 1, 40)
    # slide_content_zh = pdfparser(sys.argv[3], 1, 40)
    pdf_content = re.sub(r'[^\w\s]', '', pdf_content)
    slide_content_en = re.sub(r'[^\w\s]', '', slide_content_en)
    # seg_list = jieba.cut(slide_content_zh, cut_all=False)
    # print(" ".join(seg_list))

    os.remove(sys.argv[4]) if os.path.exists(sys.argv[4]) else None
    with open(sys.argv[4], 'w') as f:
        f.write(pdf_content)
        f.write(slide_content_en)
