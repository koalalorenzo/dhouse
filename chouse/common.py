import urllib2
from xml.dom import minidom

#IP-based Geolocation
IP_URL ="http://freegeoip.net/xml/"
def get_coords(ip):
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError: #no coordinates
        return
    logging.info("GETCOORDS")
    logging.info(content)
    if content:
        #parse the xml and find the coordinates
        g = minidom.parseString(content)
        lat = g.getElementsByTagName('Latitude')[0].childNodes[0].nodeValue
        lon = g.getElementsByTagName('Longitude')[0].childNodes[0].nodeValue
        logging.info(lat)
        return db.GeoPt(lat, lon) #GAE datatype for coordinates

#give the coordinates to Gmap
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    for p in points:
        markers = '&'.join('markers=%s,%s' % (p.lat, p.lon))
    return GMAPS_URL + markers
