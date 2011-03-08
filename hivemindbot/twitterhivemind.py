#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitterbot
import sqlite3
import feedparser
import time
import traceback
import sys

consumer_key ='' #add the customer API key here
consumer_secret = '' #add the customer API secret key here

DB_PATH = ''

class TwitterHiveMind(twitterbot.Bot):
    def hiveTweet(self,message):
        
        a.initUsername()
        print "Tweeting on " + a.getUsername()
        a.Tweet(message)
        
        
class RssTrigger():
    '''
    classdocs
    '''
    
    def debug(self,message):
        '''
        Print a debug message
        '''
        try:    
            output= time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime()) + str(message)
        except UnicodeEncodeError:
            output= time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime()) + str(message.encode("utf-8"))
        print output
        return
    
    def peridocCheck(self,searchFunc,func,seconds):
        oldResults = searchFunc()

        while self.running:
            try:
                #get new results
                newResults = [];
                newResults =searchFunc()
                
                mentions = [];
                
                for newResult in newResults:
                    found = False;
                    for oldResult in oldResults:
                        if oldResult.id == newResult.id:
                            found = True;
                            break;
                        
                    if not found:
                        mentions.append(newResult)
                
                oldResults = newResults
                
                for tweet in mentions:
                    func(tweet)
            except:
                traceback.print_exc(file=sys.stdout)
                self.debug("failed to pull url: at peridocCheck")
            time.sleep(seconds)
        return
    
    def getRss(self):
        #19065027
        #240003849
        d = feedparser.parse("https://twitter.com/statuses/user_timeline/240003849.rss")
        return d.entries
        
        
        return
        
    
    def __init__(self):
        '''
        Constructor
        '''
        self.running = True
        
        self.peridocCheck(self.getRss, hiveTweet,30)

def hiveTweet(item):
    print item.id
    id = item.id.split("statuses/")[1]
    print item.title
    
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
          
        sql = "select * from auth"
        variables=([])
        c.execute(sql,variables)
      
        for row in c:
            rowid = row[0]
            key1 = row[1]
            key2 = row[2]
            a = TwitterHiveMind(key1,key2)
            id = int(id)
            a.hiveRetweet(id)
    except:
        pass
    c.close()
    c.close()
        
    
    return

if __name__ == '__main__':
    a = RssTrigger()

        
    
