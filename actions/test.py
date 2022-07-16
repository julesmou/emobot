# from geopy import geocoders 
# from geopy.geocoders import Nominatim 
# from tzwhere import tzwhere


# def get_local_zone(city):
#     tz = tzwhere.tzwhere()
#     loc = Nominatim(user_agent="GetLoc") 
#     getLoc = loc.geocode(str(city))
#     return(tz.tzNameAt(getLoc.longitude, getLoc.lattitude))

# from timezonefinder import TimezoneFinder

# tf = TimezoneFinder()
# loc = Nominatim(user_agent="GetLoc") 
# getLoc = loc.geocode('Paris')
# print(tf.timezone_at(lng=getLoc.longitude, lat=getLoc.latitude))
import datetime
from datetime import datetime
from time import strftime
import time
print(time.strftime('%H:%M:%S', time.localtime()))