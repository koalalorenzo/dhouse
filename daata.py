from chouse import Poi
from chouse.conf import *
import foursquare

foursquare_client = foursquare.Foursquare(client_id=FOURSQUARE_API_CLIENT_ID, client_secret=FOURSQUARE_API_CLIENT_SECRET)


enlabs = Poi("41.90464064950719", "12.499051094055176")
metro_marconi = Poi("41.8493344", "12.4755884")
uni = Poi("41.8562461", "12.4688934")

enlabs.get_foursquare_vote(foursquare_client)
enlabs.analysis_data
