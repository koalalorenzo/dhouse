from chouse import Poi
from chouse.conf import *
import foursquare
from pymongo import Connection, ASCENDING, DESCENDING

db_connection =  Connection("ds043987.mongolab.com", 43987, network_timeout=30, socketTimeoutMS=20000, connectTimeoutMS=30000)
db = db_connection["heroku_app9641020"]
db.authenticate("chouseServer","genericpassword")

enlabs = Poi("41.89954600592677", "12.502334117889404")
uni = Poi("41.85556186229819", "12.470297813415527")

enlabs.database = db
uni.database = db

uni.title = "Open Space Roma 3"
uni.cap = "00145"
uni.energetic_class = "d"
uni.link = "http://www.uniroma3.it/"
uni.description = "Deep inside the most important university of Rome, this place is really important for startups and ideas"

enlabs.title = "Bellissimo Open Space Termini"
enlabs.cap = "00185"
enlabs.energetic_class = "e"
enlabs.link = "http://enlabs.it"
enlabs.description = "Cool place for startups"

enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/1.JPG", "description":"wide area", "title": "Wide Area" })

enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/2.JPG",  "description":"wide area", "title": "Wide Area" })
                    
enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/3.JPG", "description":"wide area","title": "Wide Area" })
                    

enlabs.calculate_value()
uni.calculate_value()

uni.save()
enlabs.save()

