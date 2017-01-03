#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import gensim
import os
import pandas as pd
import ast
import re
import json
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")

def process_pdf_json(path, done_path):
    with open(path) as f:
        pdf_txt = json.load(f)
        page_dict = {}
        for page in pdf_txt:
            order_dict = {}
            for order in pdf_txt[page]:
                word_size_dict = {}
                word = re.sub(r'[\u4e00-\u9fff]+', '', pdf_txt[page][order][0])
                word = re.sub(r'[().,…:@]+', ' ', word)
                size = pdf_txt[page][order][1]
                word_arr = word.split(' ')
                fit_word_arr = [x for x in word_arr if len(x) != 1 and x]
                fit_word_arr = [y for y in fit_word_arr if y not in cachedStopWords]
                if fit_word_arr:
                    word_size_dict[size] = fit_word_arr
                    order_dict[int(order)] = word_size_dict
            page_dict[int(page)] = order_dict
    f.close()
    with open(done_path + '1.json', 'w') as outfile:
        json.dump(page_dict, outfile)
    outfile.close()
    return page_dict

if __name__ == '__main__':
    pdf_txt_path = 'course/908/slide/1/1_en.json'
    pdf_json_path = 'course/908/slide_done/1/'
    pdf_dict = process_pdf_json(pdf_txt_path, pdf_json_path)
