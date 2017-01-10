#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

if len(sys.argv) < 3:
    print('Usage: python combine_ebook.py book_new/combine_1_2.en.text book_new/computernetwork-3.en.text')
    sys.exit()

def combine_book(book1, book2):
    fin = open(book1, "r")
    data1 = fin.read()
    fin.close()
    fin = open(book2, "r")
    data2 = fin.read()
    fin.close()
    combined_data = data1 + data2
    fout = open("book_new/combine_1_2_3.en.text", "w")
    fout.write(combined_data)
    fout.close()


if __name__ == '__main__':
    combine_book(sys.argv[1], sys.argv[2])
