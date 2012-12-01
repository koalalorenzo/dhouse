from chouse import Poi
from chouse.conf import *
import foursquare

foursquare_client = foursquare.Foursquare(client_id=FOURSQUARE_API_CLIENT_ID, client_secret=FOURSQUARE_API_CLIENT_SECRET)
x = Poi()

#Via vasca navale:
#x.cordinates['x'] = "41.8562461"
#x.cordinates['y'] = "12.4688934"
#Metro Marconi
#x.cordinates['x'] = "41.8493344"
#x.cordinates['y'] = "12.4755884"
#Enlabs:
x.cordinates['x'] = "41.90464064950719"
x.cordinates['y'] = "12.499051094055176"

x.get_foursquare_vote(foursquare_client)
x.analysis_data
