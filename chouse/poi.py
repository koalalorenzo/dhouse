#!/usr/bin/python
import json
import foursquare
from chouse.metwit import *
from chouse.conf import *
from django.utils.encoding import smart_str

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
                                    "radius": "1000",
                                    "intent": "browse",
                                    })['venues']
        green = 25
        times = 1
        near_place = dict()
        near_place['location'] = dict()
        near_place['location']['distance'] = 0
        near_place['referralId'] = None
        near_place['name'] = ""
        
        near_station = dict()
        near_station['location'] = dict()
        near_station['location']['distance'] = 0
        near_station['referralId'] = None
        near_station['name'] = ""
        
        near_plaza = dict()
        near_plaza['location'] = dict()
        near_plaza['location']['distance'] = 0
        near_plaza['referralId'] = None
        near_plaza['name'] = ""
        
        for venue in venues:
            print smart_str(venue['name']), ":"
            is_green = False
            for category in venue['categories']:
                print smart_str(category['shortName'])
                s_category = category['shortName'].lower()
                
                if "plaza" in s_category or "outdoor" in s_category:
                    green +=80
                    times += 1
                    if int(near_plaza['location']['distance']) < int(venue['location']['distance']):
                        self.analysis_data['Outdoor place'] = "( %sm ) %s" % ( venue['location']['distance'], venue['name'])
                        near_plaza = venue
                    is_green = True
                    
                elif "historyc" in s_category or "fountain" in s_category:
                    green +=80
                    times += 1
                    is_green = True
                        
                elif "station" in s_category or "bus" in s_category:
                    green +=75
                    times += 1
                    if int(near_station['location']['distance']) < int(venue['location']['distance']):
                        self.analysis_data['Public station'] = "( %sm ) %s" % ( venue['location']['distance'], venue['name'])
                        near_station = venue
                    is_green = True

                elif "subway" in s_category or "metro" in s_category.lower():
                    green +=75
                    times += 1
                    if int(near_station['location']['distance']) < int(venue['location']['distance']):
                        self.analysis_data['Public station'] = "( %sm ) %s" % ( venue['location']['distance'], venue['name'])
                        near_station = venue
                    is_green = True

                elif "school" in s_category or "univer" in s_category.lower():
                    green +=70
                    times += 1
                break
                
            print "----"

            if is_green:
                if int(near_place['location']['distance']) < int(venue['location']['distance']):
                    if venue["referralId"] != near_station['referralId'] or venue['referralId'] != near_plaza['referralId']:
                        near_place = venue
    
        if not near_place['name'] == "":
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
        