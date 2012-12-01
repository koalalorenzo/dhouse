import simplejson
import requests

#HTTPS

# POST api.metwit.com/token 
# INPUT: BasiAuth, FORM { "grant_type": "client_credentials" }
# BasicAuth = username : 129380295 , password: -N5rCG100xR0SOX1oqan8eZ9L2lraBmkk6_Y4aIp
# Output {"access_token"}

# GET api.metwit.com/v2/weather/?location_lat=44&location_lng=10
# header Authorization: Bearer <access_token>
# Output {"weather"

