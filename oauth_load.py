#! /usr/bin/python
# -*- coding: utf-8 -*-

# This is our Brightcove "module" containing both our oAuth procedure and the functions necessary for working with Brightcove's
# Dynamic Ingest API

print "Content-type: application/json\n\n"

import httplib
import urllib
import base64
import json
import requests


# Read the oauth secrets and account ID from our oauth configuration file "brightcove_oauth.txt" located in
# same directory as our Python scripts

def loadSecret():
    credsFile = open('brightcove_oauth.txt')
    creds = json.load(credsFile)
    return creds

# get the oauth 2.0 token


def getAuthToken(creds):
    conn = httplib.HTTPSConnection("oauth.brightcove.com")
    url = "/v3/access_token"
    params = {
        "grant_type": "client_credentials"
    }
    client = creds["client_id"]
    client_secret = creds["client_secret"]
    authString = base64.encodestring(
        '%s:%s' %
        (client, client_secret)).replace(
        '\n', '')
    requestUrl = url + "?" + urllib.urlencode(params)
    headersMap = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + authString
    }
    conn.request("POST", requestUrl, headers=headersMap)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        result = json.loads(data)
        return result["access_token"]
