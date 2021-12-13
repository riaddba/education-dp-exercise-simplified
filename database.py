#!/usr/bin/env python

import pymongo

class MongoDatabase(object):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['education-dp']
           

    