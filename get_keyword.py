#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
import pandas as pd

def ishan(text):
    # for python 3.x
    # sample: ishan('一') == True, ishan('我&&你') == False
    return all('\u4e00' <= char <= '\u9fff' for char in text)

def chid_to_order(path):
    df = pd.read_csv(path, header=None, usecols=[1,2])
    dict_ = df.set_index([1]).to_dict()
    return dict_[2]

def txtparser(order, ori_path, des_path_en, des_path_zh):
    for chid_txt in os.listdir(ori_path):
        chid = int(chid_txt.split('.')[0])
        with open(ori_path + chid_txt, 'r') as fr:
            text_content = fr.read()
            dict_content = ast.literal_eval(text_content)
        fr.close()
        os.remove(des_path_zh + str(order[chid]) + '_zh.txt') if os.path.exists(des_path_zh + str(order[chid]) + '_zh.txt') else None
        os.remove(des_path_en + str(order[chid]) + '_en.txt') if os.path.exists(des_path_en + str(order[chid]) + '_en.txt') else None
        for key in dict_content:
            if ishan(key):
                with open(des_path_zh + str(order[chid]) + '_zh.txt', 'a') as fw_zh:
                    print(key, file=fw_zh)
            else:
                with open(des_path_en + str(order[chid]) + '_en.txt', 'a') as fw_en:
                    print(key, file=fw_en)
        fw_zh.close()
        fw_en.close()


if __name__ == '__main__':
    txt_path = 'course/908/ori_keyword/'
    parser_path_en = 'course/908/keyword/en/'
    parser_path_zh = 'course/908/keyword/zh/'
    v_chap_video = 'course/908/v_chapter_video.csv'
    order = chid_to_order(v_chap_video)
    txtparser(order, txt_path, parser_path_en, parser_path_zh)
