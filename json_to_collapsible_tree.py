#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def load_json(path):
    with open(path) as data_file:
        data = json.load(data_file)

if __name__ == '__main__':
    path = 'data.json'
    load_json(path)
