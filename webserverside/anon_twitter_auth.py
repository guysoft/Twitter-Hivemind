#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3

# parse_qsl moved to urlparse module in v2.6
try:
  from urlparse import parse_qsl
except:
  from cgi import parse_qsl

import oauth2 as oauth

#import Transliterate
import cgitb
import cgi
import time


cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print


from twitter_server_config import *

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

'''
def getToken():
		auth = tweepy.OAuthHandler(consumer_key,consumer_secret )
		
		try:
			redirect_url = auth.get_authorization_url()
		except tweepy.TweepError:
			print 'Error! Failed to get request token.'
			
		return redirect_url
'''
def getOauthToken():
	signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
	oauth_consumer             = oauth.Consumer(key=consumer_key, secret=consumer_secret)
	oauth_client               = oauth.Client(oauth_consumer)
	resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')
	
	request_token = dict(parse_qsl(content))
	
	if resp['status'] == '200':
		return request_token['oauth_token'], request_token['oauth_token_secret']
	else:
		print "error getting token"
	return
		
		

def store(sid,token,oauth_token_secret):
	
	conn = sqlite3.connect(DB_PATH)
	
	c = conn.cursor()
	
	#remove previous attempts
	sql = "delete from preauth  where sid=?"
	
	
	variables = (sid,)
	c.execute(sql,variables)
	
	
	c.close()
	
	
	c = conn.cursor()
	
	# Insert a row of data
	sql = "insert into preauth  values (?,?,?)"
	variables = (oauth_token_secret,sid,token)
	
	c.execute(sql,variables)	
	# Save (commit) the changes
	conn.commit()
	

	
	# We can also close the cursor if we are done with it
	c.close()
	
	
	
	
	return

def getTokenUrl(sid):
	oauth_token,oauth_token_secret = getOauthToken()
	store(sid,oauth_token,oauth_token_secret)
	
	
	print '%s?oauth_token=%s' % (AUTHORIZATION_URL, oauth_token)
	
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
sid =  str(time.time())

if sid!= None:
	#print phone
	
	getTokenUrl(sid)
	
	#create a token and add to db

    
else:
  print sid
