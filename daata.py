from chouse import Poi
from chouse.conf import *
import foursquare

foursquare_client = foursquare.Foursquare(client_id=FOURSQUARE_API_CLIENT_ID, client_secret=FOURSQUARE_API_CLIENT_SECRET)
x = Poi()
x.cordinates['x'] = "41.8562461"
x.cordinates['y'] = "12.4688934"
x.get_foursquare_vote(foursquare_client)
x.analysis_data
