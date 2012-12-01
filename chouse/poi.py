#!/usr/bin/python
import json
import foursquare
from chouse.metweet import API
from chouse.conf import *

foursquare_client = foursquare.Foursquare(client_id='TXRYPUX0100TCJG0R3ZVLNKA0YFHCVGJDCDRUMI4EY25TEU0', client_secret='IPI0ESJWVZSBCJZINMVSLGUWPNAZEE2F2DCSOPEYD2KCQ5PA')

class Poi(object):
    def __init__(self):
        self.database = None
        self.id = None
        
        self.cordinates = dict() # { "x": "0.0" , "y": "0.0" }
        self.description = str()
        self.link = str()
        
        self.grenn = int()
        self.analysis_data = dict() # Output of analysis.
        
    def __get_rest_json_api(self, url):
        """This functions gets json data from RESTful API"""
        return dict()
        
    
    def foursquare
        
        
    def load(self):
        search = self.database.houses.find_one({"id": self.id})
        if search:
           self.by_dictionary(search)
        
    def by_dictionary(self, dictionary):
        self.id = dictionary['id']
        
    def save(self):
        search = self.database.houses.find_one({"id": self.id})
        dictionary = self.__dict__(old=search)
        self.database.houses.save(dictionary)

        return
        
    def __dict__(self, old=None):
        if not old:
            old = dict()
            
        if not old.has_key("id"):
            old['id'] = self.id
        
        return old
        