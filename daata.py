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
uni.description = """Open space office 200mq large in Marconi. This is a stunning office space. With windows on four sides, private terrace, and a high end build-out, this is truly a rare find ID 3465"""

enlabs.title = "Bellissimo Open Space Termini"
enlabs.cap = "00185"
enlabs.energetic_class = "e"
enlabs.link = "http://enlabs.it"
enlabs.description = """Spacious Open Loft 1000mq large In Termini.<br/>This spacious loft has an entire wall of windows and gets great natural light, hardwood floors and high ceiling. 24/7 access, 6 passenger elevators, freight elevator, secure lobby, close to transportation. Please reference listing ID 259"""

enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/1.JPG", "description":"wide area", "title": "Wide Area" })

enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/2.JPG",  "description":"wide area", "title": "Wide Area" })
                    
enlabs.photos.append({ "url":"https://dl.dropbox.com/u/1145876/enlabs/open/3.JPG", "description":"wide area","title": "Wide Area" })
                    

enlabs.calculate_value()
uni.calculate_value()

uni.save()
enlabs.save()

