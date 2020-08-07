# -*- coding: utf-8 -*-
"""
       (`-()_.-=-.
       /66  ,  ,  \
     =(o_/=//_(   /======`
         ~"` ~"~~`        C.E.
         
Created on Thu Aug  6 11:58:53 2020
@author: Chris
Contact :
    Christopher.eaby@gmail.com
"""

import tweepy
import matplotlib.pyplot as plt
import folium
import numpy as np
from geopy.geocoders import Nominatim
import tkinter as tk
import webbrowser

geolocator = Nominatim(user_agent="Twitter-mining")

consumerkey = "chppDoy3i8wZTLCy7eZDkSopJ"
consumersecret = "ur0MVNOyvBKHponM0rhO6KNgRsith3LKeSOo0C5qD6anfa4NH6"
accesstoken = "1291306417287307264-pvZ3yK8ksdvW4j2kNMw6SAnu8YHZtP"
accesstokensecret = "YdEZ2111JFXJ0SgboeNVwjPOSrINYMc9ATo0ivaaAunPj"

auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesstoken, accesstokensecret)
api = tweepy.API(auth)

fgv = folium.FeatureGroup(name = "Tweets")

map1 = folium.Map(location = [0, 0], zoom_start = 2)
fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

def gettweets(tweettype, amount):
    data = []
    results = api.search(q = tweettype, lang = "en", count = amount)
    results = np.array(results)
    for tweet in results:
        tweet_details = {}
        tweet_details['Date'] = tweet.created_at.date()
        tweet_details['Time'] = tweet.created_at.time().strftime('%H:%M:%S')
        tweet_details['Tweet'] = tweet.text
        tweet_details['Username'] = tweet.user.screen_name
        try:
            loc = geolocator.geocode(tweet.user.location)
            tweet_details['Location'] = (loc.latitude, loc.longitude)
        except:
            tweet_details['Location'] = ''
        data.append(tweet_details)
        
    return(data)

def makepltndworld(tweettype, amount):
    counter = 0
    for item in gettweets(tweettype, amount):
        counter += 1
        plt.plot(counter, item['Date'], 'go-')
        if item['Location'] != '':
            fgv.add_child(folium.CircleMarker(location = item['Location'], radius = 6, fill_opacity = 0.7, popup = (str(item['Date']) + "\n" + item['Username'] + "\n" + item['Tweet']), fill_color = 'orange', color = 'black'))
        else:
            pass

gui = tk.Tk()
# sets the title 
gui.title("Twitter Mining")
# sets the size
gui.geometry("250x130")

txt1 = tk.Text(gui, fg = "white", bg = "purple", height = 1, width = 15)
txt1.grid(row = 4, column = 1)
lbl5 = tk.Label(gui, text = "Query", justify = tk.CENTER, padx = 30, pady = 10)
lbl5.grid(row = 4, column = 0)
txt2 = tk.Text(gui, fg = "white", bg = "purple", height = 1, width = 15)
txt2.grid(row = 5, column = 1)
lbl6 = tk.Label(gui, text = "Amount", justify = tk.CENTER, padx = 30, pady = 10)
lbl6.grid(row = 5, column = 0)
b1 = tk.Button(gui, text = "Search", height = 2, width = 9, command = lambda: makepltndworld(txt1.get("1.0","end"), (txt2.get("1.0","end"))))
b1.grid(row = 6, column = 0)    
    
gui.mainloop()   

map1.add_child(fgp)
map1.add_child(fgv)
map1.add_child(folium.LayerControl())
map1.save("tweets.html") 
new = 2
webbrowser.open('tweets.html', new = new)

plt.xticks(rotation = 15, color='blue', size=13)
plt.yticks(rotation = 15, color='blue', size=13)
plt.xlabel('Amount of tweets', {'color':'grey', 'fontsize':15})
plt.ylabel('Date', {'color':'grey', 'fontsize':15})
plt.show()                                                                                                                                                                                                                                                                                                                                                                                                                                                                #alex helped a bit