from chouse import Poi
from chouse.conf import *
import foursquare

foursquare_client = foursquare.Foursquare(client_id=FOURSQUARE_API_CLIENT_ID, client_secret=FOURSQUARE_API_CLIENT_SECRET)


enlabs = Poi("41.89954600592677", "12.502334117889404")
metro_marconi = Poi("41.8493344", "12.4755884")
uni = Poi("41.85556186229819", "12.470297813415527")

enlabs.get_foursquare_vote(foursquare_client)
enlabs.analysis_data
