import requests
import json
import configparser
import time
from datetime import datetime

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args

# See https://www.space-track.org/documentation for details on REST queries
# the "Find Starlinks" query searches all satellites with NORAD_CAT_ID > 40000, with OBJECT_NAME matching STARLINK*, 1 line per sat
# the "OMM Starlink" query gets all Orbital Mean-Elements Messages (OMM) for a specific NORAD_CAT_ID in JSON format

uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query"
requestOMMStarlink1    = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2    = "/orderby/NORAD_CAT_ID%20asc/format/tle"   


# Use configparser package to pull in the ini file (pip install configparser)
config = configparser.ConfigParser()
config.read("./SLTrack.ini")
configUsr = config.get("configuration","username")
configPwd = config.get("configuration","password")
siteCred = {'identity': configUsr, 'password': configPwd}

def getTLESatellites(date):
    requestFindStarlinks   = f'/class/tle/NORAD_CAT_ID/>00000/EPOCH/{date}/orderby/~~/format/3le/orderby/NORAD_CAT_ID%20asc'
    # use requests package to drive the RESTful session with space-track.org
    with requests.Session() as session:
        # run the session in a with block to force session to close if we exit

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "POST fail on login")

        # this query picks up TLEs for all satellites from the catalog. Note - a 401 failure shows you have bad credentials 
        resp = session.get(uriBase + requestCmdAction + requestFindStarlinks)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "GET fail on request for satellites")

        # resp.text contains TLEs for all the satellies in that given EPOCH 
        satellites = resp.text
        session.close()
    return satellites 




                