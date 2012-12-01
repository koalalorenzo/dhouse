import simplejson
import requests

#HTTPS

# POST api.metwit.com/token 
# INPUT: BasiAuth, FORM { "grant_type": "client_credentials" }
# BasicAuth = username : clientID , password: client_secret
# Output {"access_token"}

# GET api.metwit.com/v2/weather/?location_lat=44&location_lng=10
# header Authorization: Bearer <access_token>
# Output {"weather"

