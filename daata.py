from chouse import Poi
from chouse.conf import *
import foursquare
from pymongo import Connection, ASCENDING, DESCENDING

db_connection =  Connection("localhost", 27017, network_timeout=30, socketTimeoutMS=20000, connectTimeoutMS=30000)
db = db_connection["app9597564"]


enlabs = Poi("41.89954600592677", "12.502334117889404")
uni = Poi("41.85556186229819", "12.470297813415527")

enlabs.database = db
uni.database = db

uni.cap = "00145"
enlabs.cap = "00185"

enlabs.calculate_value()
uni.calculate_value()

uni.save()
enlabs.save()