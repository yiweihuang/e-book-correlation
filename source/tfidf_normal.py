#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import numpy as np

def create_normal(path):
    for f in os.listdir(path):
        if fnmatch.fnmatch(f, '*result.txt'):
            normal_arr = []
            temp_dict = {}
            with open(path + f, 'r') as fr:
                for line in fr:
                    normal_arr.append(float(line.split('\t')[1].split('\n')[0]))
                    temp_dict[line.split('\t')[0]] = float(line.split('\t')[1].split('\n')[0])
            mu = np.average(normal_arr)
            final_mu = round(mu)
            fr.close()
            new_f = f.split('_')[0]
            os.remove(path + new_f + '_normal.txt') if os.path.exists(path + new_f + '_normal.txt') else None
            with open(path + new_f + '_normal.txt', 'w') as fw:
                for key in sorted(temp_dict, key=temp_dict.get, reverse=True):
                    if int(temp_dict[key]) >= final_mu:
                        fw.write('%s\t%s\n' % (key, temp_dict[key]))

if __name__ == '__main__':
    tfidf_path = 'course/908/NS/'
    create_normal(tfidf_path)
