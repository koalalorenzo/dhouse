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

uni.title = "OpenSpace Roma 3"
uni.cap = "00145"
uni.energetic_class = "d"

enlabs.title = "Bellissimo Open Space Termini"
enlabs.cap = "00185"
enlabs.energetic_class = "e"

enlabs.calculate_value()
uni.calculate_value()

uni.save()
enlabs.save()
