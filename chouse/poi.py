#!/usr/bin/python
import json
import foursquare
from chouse.metwit import *
from chouse.conf import *
from django.utils.encoding import smart_str
from hashlib import sha1

class Poi(object):
    def __init__(self, lat, lng):
        self.database = None
        self.id = sha1("%s%s" % (lat, lng)).hexdigest() 
                
        self.coordinates = {"lat": lat, "lng": lng}
        self.cap = str()
        self.street = str()
        self.photos = list() 
        self.price = int()
        
        self.title = str()
        self.description = str()
        self.link = str()
        self.energetic_class = str() # a - g
                
        self.green = int() # Value of "green" 1-100
        self.analysis_data = dict() # Output of analysis.
    
    def get_foursquare_vote(self, fsq):
        venues = fsq.venues.search({
                                    "ll":"%s,%s" % (self.coordinates['lat'], self.coordinates['lng']),
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
        
        near_outdoor = dict()
        near_outdoor['location'] = dict()
        near_outdoor['location']['distance'] = 1500
        near_outdoor['referralId'] = None
        near_outdoor['name'] = ""

        near_plaza = dict()
        near_plaza['location'] = dict()
        near_plaza['location']['distance'] = 1500
        near_plaza['referralId'] = None
        near_plaza['name'] = ""
        
        for venue in venues:
            is_green = False
            for category in venue['categories']:
                s_category = smart_str(category['shortName']).lower()
                
                if "field" in s_category or "outdoor" in s_category: # EX: soccer field or outdoor
                    if int(near_outdoor['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Outdoor place"] = "%s ( %s  %sm )" % ( venue['name'], s_category, venue['location']['distance'] )
                        near_outdoor = venue
                    green += 80
                    times += 1
                    is_green = True
                    
                elif "historyc" in s_category or "fountain" in s_category:
                    green += 60
                    times += 1
                    is_green = True

                elif "plaza" in s_category:
                    green += 60
                    times += 1
                    if int(near_plaza['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Plaza"] = "%s at <b>%sm</b> " % (venue['name'],  venue['location']['distance'])
                        near_outdoor = venue
                    is_green = True
                        
                elif "station" in s_category or "bus" in s_category:
                    green += 50
                    times += 1
                    if int(near_station['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Public Transport"] = "%s at <b>%sm</b> - %s" % ( s_category, venue['location']['distance'], venue['name'] )
                        near_station = venue
                    
                elif "subway" in s_category or "metro" in s_category.lower():
                    green += 50
                    times += 1
                    if int(near_station['location']['distance']) > int(venue['location']['distance']):
                        self.analysis_data["Public Transport"] = "<b>%sm</b> to %s" % ( venue['location']['distance'], venue['name'] )
                        near_station = venue
                    
                elif "school" in s_category or "univer" in s_category.lower():
                    green += 40
                    times += 1
                    
                elif "hospital" in s_category:
                    green += 30
                    times += 1
               
            if is_green:
                if int(near_place['location']['distance']) > int(venue['location']['distance']):
                    if venue["referralId"] != near_station['referralId'] and venue['referralId'] != near_outdoor['referralId'] and venue['referralID'] != near_plaza['referralId']:
                        near_place = venue
    
        if near_place['referralId']:
            self.analysis_data['Other'] = "%s at <b>%sm</b>: %s" % ( smart_str(near_place['categories'][0]['shortName']), near_place['location']['distance'], near_place['name'] )
        
        return int(green/times) # Media
        
    def get_nox_by_cap(self):
        if self.cap == "00145":
            self.analysis_data['Pollution level ( N02 )'] = "<b>196 mcg/m3</b> ( Risky )"
            return 62
        elif self.cap == "00185":
            self.analysis_data['Pollution level ( N02 )'] = "<b>110 mcg/m3</b> ( Average )"
            return 62
        
    def get_pm10_by_cap(self):
        if self.cap == "00145":
            self.analysis_data['Pollution level ( PM10 )'] = "<b>33 mcg/m3</b> ( Acceptable )"
            return 30
        elif self.cap == "00185":
            self.analysis_data['Pollution level ( PM10 )'] = "<b>37 mcg/m3</b> ( Acceptable )"
            return 20
    
    def get_grass_dencity_by_cap(self):
        if self.cap == "00145":
            self.analysis_data['Green density'] = "<b>62,2%</b> ( Above average )"
            self.analysis_data['Green per person'] = "<b>216,7 m3</b> ( Into the wild )"
            return 62
        elif self.cap == "00185":
            self.analysis_data['Green density'] = "<b>9,2%</b> ( Very poor )"
            self.analysis_data['Green per person'] = "<b>10 m3</b> ( Low )"
            return 9

    def get_value_by_energetic_class(self):
        self.analysis_data["Building Energetic Class"] = "%s" % self.energetic_class.upper()
        if self.energetic_class == "a":
            return 90
        elif self.energetic_class == "b":
            return 80
        elif self.energetic_class == "c":
            return 70
        elif self.energetic_class == "d":
            return 60
        elif self.energetic_class == "e":
            return 50
        elif self.energetic_class == "f":
            return 40
        elif self.energetic_class == "g":
            return 30
        else:
            return 20
      
    def calculate_value(self):
        self.green = 0
        total = 0
        
        foursquare_client = foursquare.Foursquare(
                client_id=FOURSQUARE_API_CLIENT_ID,
                client_secret=FOURSQUARE_API_CLIENT_SECRET)

        total += self.get_foursquare_vote(foursquare_client)
        total += self.get_nox_by_cap()
        total += self.get_pm10_by_cap()
        total += self.get_grass_dencity_by_cap()
        total += self.get_value_by_energetic_class()
        
        self.green = int(total/5)
        return self.green
        
    def load(self):
        search = self.database.houses.find_one({"id": self.id})
        if search:
           self.by_dictionary(search)
        return self
        
    def by_dictionary(self, dictionary):
        self.id = dictionary['id']
        
        self.coordinates = dictionary['coordinates']
        self.cap = dictionary['cap']
        self.street = dictionary['street']
        self.photos = dictionary['photos']
        self.price = int(dictionary['price'])
        
        self.title = dictionary['title']
        self.description = dictionary['description']
        self.link = dictionary['link']
        self.energetic_class = dictionary['energetic_class']
        
        self.green = int(dictionary['green'])
        self.analysis_data = dictionary['analysis_data']
        return self

    def save(self):
        search = self.database.houses.find_one({"id": self.id})
        dictionary = self.__dict__(old=search)
        self.database.houses.save(dictionary)

        return
        
    def __dict__(self, old=None):
        if not old:
            old = dict()

        if not self.id:
            self.id = sha1("%s%s" % ( self.coordinates['lat'], self.coordinates['lng'])).hexdigest()            
        
        if not old.has_key("id"):
            old['id'] = self.id
        
        
        old['coordinates'] = self.coordinates
        old['cap'] = self.cap
        old['street'] = self.street
        old['photos'] = self.photos
        old['price'] = self.price
        
        old['title'] = self.title
        old['description'] = self.description
        old['link'] = self.link
        old['energetic_class'] = self.energetic_class
        
        old['green'] = self.green
        old['analysis_data'] = self.analysis_data
        
        return old
        