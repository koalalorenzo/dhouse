#!/usr/bin/python
import json
import foursquare
from chouse.metwit import *
from chouse.conf import *
from django.utils.encoding import smart_str

class Poi(object):
    def __init__(self, lat, lng):
        self.database = None
        self.id = None
        
        self.cordinates = {"lat": lat, "lng": lng}
        self.description = str()
        self.link = str()
        
        self.grenn = int() # Value of "green" 1-100
        self.analysis_data = dict() # Output of analysis.
        
    def __get_rest_json_api(self, url):
        """This functions gets json data from RESTful API"""
        return dict()
        
    
    def get_foursquare_vote(self, fsq):
        venues = fsq.venues.search({
                                    "ll":"%s,%s" % (self.cordinates['lat'], self.cordinates['lng']),
                                    "limit": 50,
                                    "radius": "800",
                                    "intent": "browse",
                                    })['venues']
        green = 25
        times = 0
        near_place = dict()
        near_place['location'] = dict()
        near_place['location']['distance'] = 1500
        near_place['referralId'] = None
        near_place['name'] = ""
        
        near_station = dict()
        near_station['location'] = dict()
        near_station['location']['distance'] = 1500
        near_station['referralId'] = None
        near_station['name'] = ""
        
        near_plaza = dict()
        near_plaza['location'] = dict()
        near_plaza['location']['distance'] = 1500
        near_plaza['referralId'] = None
        near_plaza['name'] = ""
        
        for venue in venues:
            is_green = False
            for category in venue['categories']:
                s_category = smart_str(category['shortName']).lower()
                if "plaza" in s_category:
                    green += 80
                    times += 1
                    if int(near_plaza['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Plaza"] = "( %sm ) %s" % ( venue['location']['distance'], venue['name'])
                        near_plaza = venue
                    is_green = True
                
                elif "field" in s_category or "outdoor" in s_category: # EX: soccer field or outdoor
                    if int(near_plaza['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Outdoor place"] = "( %s  %sm ) %s" % ( s_category, venue['location']['distance'], venue['name'])
                        near_plaza = venue
                    green += 80
                    times += 1
                    is_green = True
                    
                elif "historyc" in s_category or "fountain" in s_category:
                    green +=80
                    times += 1
                    is_green = True
                        
                elif "station" in s_category or "bus" in s_category:
                    green +=75
                    times += 1
                    if int(near_station['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Public Transport"] = "( %s %sm ) %s" % ( s_category, venue['location']['distance'], venue['name'])
                        near_station = venue
                    
                elif "subway" in s_category or "metro" in s_category.lower():
                    green +=75
                    times += 1
                    if int(near_station['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Public Transport"] = "( %s %sm ) %s" % ( s_category, venue['location']['distance'], venue['name'])
                        near_station = venue
                    
                elif "school" in s_category or "univer" in s_category.lower():
                    green +=70
                    times += 1
            
            if is_green:
                if int(near_place['location']['distance']) > int(venue['location']['distance']):
                    if venue["referralId"] != near_station['referralId'] and venue['referralId'] != near_plaza['referralId']:
                        near_place = venue
    
        if near_place['referralId']:
            self.analysis_data['Other'] = "( %s %sm ) %s" % ( smart_str(near_place['categories'][0]['shortName']), near_place['location']['distance'], near_place['name'] )
        
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
        