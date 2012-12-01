#!/usr/bin/python
import json
import foursquare
from chouse.metweet import *
from chouse.conf import *

class Poi(object):
    def __init__(self):
        self.database = None
        self.id = None
        
        self.cordinates = dict() # { "x": "0.0" , "y": "0.0" }
        self.description = str()
        self.link = str()
        
        self.grenn = int() # Value of "green" 1-100
        self.analysis_data = dict() # Output of analysis.
        
    def __get_rest_json_api(self, url):
        """This functions gets json data from RESTful API"""
        return dict()
        
    
    def get_foursquare_vote(self, fsq):
        venues = fsq.venues.search({
                                    "ll":"%s,%s" % (self.cordinates['x'], self.cordinates['y']),
                                    "limit": 50,
                                    "radius": 800,
                                    "intent": "browse",
                                    "near": "Roma"
                                    })['venues']
        gren = 25
        times = 1
        near_place = dict()
        near_place['location'] = dict()
        near_place['location']['distance'] = 0
        
        for venue in venues:
            if "station" in venue['name'].lower() or "bus" in venue['name'].lower():
                green += 75
                times += 1
                if int(near_place['location']['distance']) < int(venue['location']['distance']):
                    near_place = venue
                continue
                
            is_green = False
            for category in venue['categories']:
                if "plaza" in category['shortName'] or "green" in category['shortName']:
                    green +=75
                    times += 1
                    is_green = True
                        
                if "station" in category['shortName'] or "bus" in category['shortName']:
                    green +=75
                    times += 1
                    is_green = True
                    
                if "Historyc" in category['shortName'] or "bus" in category['shortName']:
                    green +=75
                    times += 1
                    is_green = True

            if is_green:
                if int(near_place['location']['distance']) < int(venue['location']['distance']):
                    near_place = venue
        
        self.analysis_data['Greener place near'] = "( %sm ) %s" % ( near_place['location']['distance'], near_place['name'])
        
        return int(green/times) # Media
        
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
        