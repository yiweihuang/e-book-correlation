#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim
import os
import pandas as pd
import ast
import json

def keyword_to_chid(path):
    text_dict = {}
    for chid_txt in os.listdir(path):
        chid = int(chid_txt.split('_')[0])
        with open(path + chid_txt, 'r') as fr:
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
            # print(word)
            # print(temp_arr)
        except:
            # print('word %s not in vocabulary' % (word))
            pass
    return word2vec_dict

def mapping_word_order(text_dict, word2vec_dict):
    learn_path = []
    keyword = text_dict.keys()
    for word in word2vec_dict:
        tempdict = {}
        intersection = set(keyword).intersection(word2vec_dict[word])
        tempdict[word] = max(text_dict[word])
        if bool(intersection):
            for wv in intersection:
                tempdict[wv] = max(text_dict[wv])
        learn_path.append(tempdict)
    return learn_path

def word_detail(txt_path, v_chap_video, learn_path):
    df = pd.read_csv(v_chap_video, header=None, usecols=[1,2])
    dict_ = df.set_index([1]).to_dict()
    arr = []
    for path_dict in learn_path:
        dict_detail = {}
        for key, value in path_dict.items():
            word_content = {}
            chid = list(dict_[2].keys())[list(dict_[2].values()).index(value)]
            with open(txt_path + str(chid) + '.txt', 'r') as fr:
                text_content = fr.read()
                dict_content = ast.literal_eval(text_content)
            fr.close()
            temparr = []
            for video_name in dict_content[key]['vid_list']:
                temparr.append(video_name[0])
            word_content['order'] = value
            word_content['video_name'] = temparr
            dict_detail[key] = word_content
        arr.append(dict_detail)
    return arr

if __name__ == '__main__':
    txt_path = 'course/908/ori_keyword/'
    word_path = 'course/908/keyword/en/'
    v_chap_video = 'course/908/v_chapter_video.csv'
    text_dict = keyword_to_chid(word_path)
    model = gensim.models.Word2Vec.load_word2vec_format("ebook_model/1_2/CBOW/computernetwork.en.text.vector", binary=False)
    word2vec_dict = keyword_to_word2vec(model, text_dict)
    # learn_path = mapping_word_order(text_dict, word2vec_dict)
    # arr = word_detail(txt_path, v_chap_video, learn_path)
    # with open('data_skip_gram.json', 'w') as outfile:
        # json.dump(arr, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
