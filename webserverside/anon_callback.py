#!/usr/bin/env python
# -*- coding: utf-8 -*-

# enable debugging
import cgitb
import tweepy
cgitb.enable()

import cgitb
import cgi
cgitb.enable()

import twitterbot
import sqlite3

print "Content-Type: text/plain;charset=utf-8"
print

from twitter_server_config import *


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields

oauth_token = form.getvalue('oauth_token')
oauth_verifier = form.getvalue('oauth_verifier')


def getKey(key,otherKey,secret):
    
  # Let's say this is a web app, so we need to re-build the auth handler
  # first...
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret,secret)
  
  auth.set_request_token(key, otherKey)

  try:
      auth.get_access_token(secret)
  except tweepy.TweepError:
      print 'Error! Failed to get access token.'
  return auth.access_token.key,auth.access_token.secret

def getDBKey(oauth_token):
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()
  
  sql = "select * from preauth where token =?"
  variables=(oauth_token,)
  c.execute(sql,variables)
  
  for row in c:#should run once
    returnValue = row[0]
    c.close()
    conn.close()
    return returnValue
  
def store(key1,key2):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	
	# Insert a row of data
	sql = "insert into auth  values (?,?,?)"
	variables = (None,key1,key2)
	
	c.execute(sql,variables)	
	# Save (commit) the changes
	conn.commit()
	
	# We can also close the cursor if we are done with it
	c.close()
	
	return

#print oauth_token , oauth_verifier

#lets get the the other auth

otherKey = getDBKey(oauth_token)

#print otherKey

key1, key2 = getKey(oauth_token,otherKey,oauth_verifier)
store(key1,key2)
