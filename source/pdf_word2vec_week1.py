#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim
import os
import ast
import re
import json
import itertools
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from collections import OrderedDict, Counter
import operator

cachedStopWords = stopwords.words("english")

def process_pdf_json(path, done_path, mode):
    with open(path) as f:
        pdf_txt = json.load(f)
        page_dict = {}
        for page in pdf_txt:
            order_dict = {}
            for order in pdf_txt[page]:
                word_size_dict = {}
                word = re.sub(r'[\u4e00-\u9fff]+', '', pdf_txt[page][order][0])
                word = re.sub(r'[().,…:@=]+', ' ', word)
                size = pdf_txt[page][order][1]
                word_arr = word.split(' ')
                fit_word_arr = [x for x in word_arr if len(x) != 1 and x]
                fit_word_arr = [y for y in fit_word_arr if y not in cachedStopWords]
                if fit_word_arr:
                    fit_concept_arr = []
                    for concept in fit_word_arr:
                        concept_dict = {}
                        try:
                            mode_arr = mode.most_similar(concept)
                            concept_dict[concept] = mode_arr
                        except:
                            pass
                        if concept_dict:
                            fit_concept_arr.append(concept_dict)
                    word_size_dict[size] = fit_concept_arr
                    order_dict[int(order)] = word_size_dict
            page_dict[int(page)] = order_dict
    f.close()
    # with open(done_path + '1.json', 'w') as outfile:
    #     json.dump(page_dict, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
    # outfile.close()
    return page_dict

def process_page_to_size(path, done_path, tfidf_path):
    with open(path) as f:
        pdf_txt = json.load(f)
        page_dict = {}
        for page in pdf_txt:
            word_size_dict = {}
            for order in pdf_txt[page]:
                word = re.sub(r'[\u4e00-\u9fff]+', '', pdf_txt[page][order][0])
                word = re.sub(r'[().,…:@=>]+', ' ', word)
                size = int(pdf_txt[page][order][1])
                word_arr = word.split(' ')
                fit_word_arr = [x for x in word_arr if len(x) != 1 and x]
                fit_word_arr = [y for y in fit_word_arr if y not in cachedStopWords]
                fit_word_arr = [y for y in fit_word_arr if y.lower() in open(tfidf_path).read().lower()]
                if fit_word_arr:
                    if word_size_dict.get(size) is None:
                        word_size_dict[size] = fit_word_arr
                    else:
                        word_size_dict[size] = word_size_dict[size] + fit_word_arr
            sort_word_size = OrderedDict(sorted(word_size_dict.items()))
            temp_tool = []
            for key in sort_word_size:
                temp_tool.append(list(set(sort_word_size[key])))
            df = pd.DataFrame(list(itertools.product(*temp_tool)))
            os.remove(done_path + 'page_to_size/' + str(final) + '.csv') if os.path.exists(done_path + 'page_to_size/' + str(final) + '.csv') else None
            df.to_csv(done_path + 'page_to_size/' + str(page) + '.csv', index=False, header=False)
    f.close()

def process_page_to_rows(path, done_path, tfidf_path):
    with open(path) as f:
        pdf_txt = json.load(f)
        page_dict = {}
        page_row_size = {}
        last_row_size = []
        for page in pdf_txt:
            word_order_dict = {}
            size_order_dict = {}
            for order in pdf_txt[page]:
                word = re.sub(r'[\u4e00-\u9fff]+', '', pdf_txt[page][order][0])
                word = re.sub(r'[().,…:@=>]+', ' ', word)
                size = int(pdf_txt[page][order][1])
                word_arr = word.split(' ')
                fit_word_arr = [x for x in word_arr if len(x) != 1 and x]
                fit_word_arr = [y for y in fit_word_arr if y not in cachedStopWords]
                fit_word_arr = [y for y in fit_word_arr if y.lower() in open(tfidf_path).read().lower()]
                if fit_word_arr:
                    word_order_dict[int(order)] = fit_word_arr
                    size_order_dict[int(order)] = size
                    page_dict[int(page)] = word_order_dict
                    page_row_size[int(page)] = size_order_dict
            sort_word_order_dict = OrderedDict(sorted(word_order_dict.items()))
            sort_size_order_dict = OrderedDict(sorted(size_order_dict.items()))
            last_row_size.append(list(sort_size_order_dict.values())[-1])
        most_common_size = Counter(last_row_size).most_common(1)[0][0]
        for final in page_dict:
            del_arr = [k for k, v in page_row_size[final].items() if v == most_common_size]
            for key_item in del_arr:
                try:
                    page_dict[final].pop(key_item, None)
                except KeyError:
                    pass
            sort_word_rows = OrderedDict(sorted(page_dict[final].items()))
            temp_tool = []
            for k in sort_word_rows:
                temp_tool.append(sort_word_rows[k])
            df = pd.DataFrame(list(itertools.product(*temp_tool)))
            os.remove(done_path + 'page_to_rows/' + str(final) + '.csv') if os.path.exists(done_path + 'page_to_rows/' + str(final) + '.csv') else None
            df.to_csv(done_path + 'page_to_rows/' + str(final) + '.csv', index=False, header=False)
    f.close()

def process_page_to_rank(path, done_path, tfidf_path):
    with open(path) as f:
        pdf_txt = json.load(f)
        page_dict = {}
        page_row_size = {}
        last_row_size = []
        first_row_size = []
        for page in pdf_txt:
            word_order_dict = {}
            size_order_dict = {}
            for order in pdf_txt[page]:
                word = re.sub(r'[\u4e00-\u9fff]+', '', pdf_txt[page][order][0])
                word = re.sub(r'[().,…:@=>]+', ' ', word)
                size = int(pdf_txt[page][order][1])
                word_arr = word.split(' ')
                fit_word_arr = [x for x in word_arr if len(x) != 1 and x]
                fit_word_arr = [y for y in fit_word_arr if y not in cachedStopWords]
                fit_word_arr = [y for y in fit_word_arr if y.lower() in open(tfidf_path).read().lower()]
                if fit_word_arr:
                    word_order_dict[int(order)] = list(set(fit_word_arr))
                    size_order_dict[int(order)] = size
                    page_dict[int(page)] = word_order_dict
                    page_row_size[int(page)] = size_order_dict
            sort_word_order_dict = OrderedDict(sorted(word_order_dict.items()))
            sort_size_order_dict = OrderedDict(sorted(size_order_dict.items()))
            last_row_size.append(list(sort_size_order_dict.values())[-1])
            first_row_size.append(list(sort_size_order_dict.values())[0])
        last_most_common_size = Counter(last_row_size).most_common(1)[0][0]
        first_most_common_size = Counter(first_row_size).most_common(1)[0][0]
        for final in page_dict:
            del_arr = [k for k, v in page_row_size[final].items() if v == last_most_common_size]
            for key_item in del_arr:
                try:
                    page_dict[final].pop(key_item, None)
                    page_row_size[final].pop(key_item, None)
                except KeyError:
                    pass
            sort_word_rows = OrderedDict(sorted(page_dict[final].items()))
            sort_size_rows = OrderedDict(sorted(page_row_size[final].items()))
            first_item_word = sort_word_rows.popitem(last = False)
            first_item_size = sort_size_rows.popitem(last = False)
            rank_arr = []
            rank = []
            for i in range(len(sort_size_rows)):
                size_arr = list(sort_size_rows)
                try:
                    if sort_size_rows[size_arr[i]] >= sort_size_rows[size_arr[i+1]]:
                        rank.append(sort_word_rows[size_arr[i]])
                    else:
                        rank.append(sort_word_rows[size_arr[i]])
                        rank.insert(0,first_item_word[1])
                        rank_arr.append(rank)
                        rank = []
                except IndexError:
                    rank.append(sort_word_rows[size_arr[i]])
                    rank.insert(0,first_item_word[1])
                    rank_arr.append(rank)
                    rank = []
                    pass
            os.remove(done_path + 'page_to_rank/' + str(final) + '.csv') if os.path.exists(done_path + 'page_to_rank/' + str(final) + '.csv') else None
            for count in rank_arr:
                df = pd.DataFrame(list(itertools.product(*count)))
                df.to_csv(done_path + 'page_to_rank/' + str(final) + '.csv', mode='a', index=False, header=False)
    f.close()

def get_small_word(dictionary):
    size_arr = []
    for page in dictionary:
        for rows in dictionary[page]:
            word_size = list(dictionary[page][rows].keys())[0]
            size_arr.append(word_size)
    return np.unique(size_arr)

def every_size_concept(dictionary, word_size):
    for page in dictionary:
        for rows in dictionary[page]:
            for i in word_size:
                with open('course/908/slide_done/1/size/' + str(i) + '.json', 'a') as outfile:
                    if i in dictionary[page][rows]:
                        json.dump(dictionary[page][rows][i], outfile, sort_keys = True, indent = 4, ensure_ascii=False)


if __name__ == '__main__':
    pdf_txt_path = 'course/908/slide/1/1_en.json'
    pdf_json_path = 'course/908/slide_done/1/'
    tfidf_path = 'course/908/NS/week1_normal.txt'
    # model = gensim.models.Word2Vec.load_word2vec_format('ebook_model/skip-gram-mark/computernetwork.en.text.vector', binary=False)
    # pdf_dict = process_pdf_json(pdf_txt_path, pdf_json_path, model) # cut sentences and filter stop word to query(Word2Vec)
    # process_page_to_size(pdf_txt_path, pdf_json_path, tfidf_path) # use the size of word to compute the product of an iterable with itself
    # process_page_to_rows(pdf_txt_path, pdf_json_path, tfidf_path) # use the order of sentences to compute the product of an iterable with itself
    process_page_to_rank(pdf_txt_path, pdf_json_path, tfidf_path) # use the order of sentences to compute the product of an iterable with itself
    # with open('course/908/slide_done/1/1.json') as reader:
    #     data = json.load(reader)
    # size = get_small_word(pdf_dict)
    # every_size_concept(pdf_dict, size) # get words of same size to product file
