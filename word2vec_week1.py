#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim
import os
import pandas as pd
import ast
import json

def keyword_to_chid(path):
    text_dict = {}
    chid_txt = path.split('/')[-1]
    chid = int(chid_txt.split('_')[0])
    with open(path, 'r') as fr:
        for text in fr:
            text = text.split('\n')[0]
            if text_dict.get(text):
                text_dict[text].append(chid)
            else:
                text_dict[text] = [chid]
    return text_dict

def keyword_to_word2vec(model, dictionary):
    word2vec_dict = {}
    for word in dictionary.keys():
        try:
            word_arr = model.most_similar(word)
            temp_arr = []
            for close_word in word_arr:
                temp_arr.append(close_word[0])
            word2vec_dict[word] = temp_arr
            print(word)
            print(temp_arr)
        except:
            # print('word %s not in vocabulary' % (word))
            pass
    return word2vec_dict

def multiple_model(cbow, skip_gram, dictionary):
    word2vec_dict = {}
    for word in dictionary.keys():
        try:
            cbow_arr = cbow.most_similar(word)
            skip_gram_arr = skip_gram.most_similar(word)
            # list(set(cbow_arr) - set(skip_gram_arr))
            temp_arr = []
            for close_word in list(set(skip_gram_arr) - set(cbow_arr)):
                temp_arr.append(close_word[0])
            word2vec_dict[word] = temp_arr
        except:
            # print('word %s not in vocabulary' % (word))
            pass
    return word2vec_dict

if __name__ == '__main__':
    txt_path = 'course/908/ori_keyword/'
    word_path = 'course/908/keyword/en/2_en.txt'
    v_chap_video = 'course/908/v_chapter_video.csv'
    text_dict = keyword_to_chid(word_path)
    model_cbow = gensim.models.Word2Vec.load_word2vec_format("ebook_model/2_3/CBOW/computernetwork.en.text.vector", binary=False)
    model_skip_gram = gensim.models.Word2Vec.load_word2vec_format("ebook_model/2_3/skip-gram/computernetwork.en.text.vector", binary=False)
    arr = multiple_model(model_cbow, model_skip_gram, text_dict)
    with open('week1/2_3/week1_skip_gram.json', 'w') as outfile:
        json.dump(arr, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
