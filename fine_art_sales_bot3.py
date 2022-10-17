# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 13:12:42 2021

@author: bpham
"""
import random
from requests_oauthlib import OAuth1Session
import time
from datetime import datetime
import pandas as pd
from tkinter import *
from tkinter import filedialog
import requests
import tweepy


consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''



##These functions help acquire access tokens and access keys to a particular twitter
##account. It creates a session in which a signed in twitter profile authenticates
##or allows this code to use the twitter api
#
##This function get's a temporary resource token so that it will be input to generate
##an authorization permision later.
#def get_resource_token():
#    
#    #create an object of OAuth1Session    
#    request_token = OAuth1Session(client_key=consumer_key,client_secret=consumer_secret)
#    
#    # twitter endpoint to get request token
#    url = 'https://api.twitter.com/oauth/request_token'
#    
#    # get request_token_key, request_token_secret and other details
#    data = request_token.get(url)
#    
#    # split the string to get relevant data 
#    data_token = str.split(data.text, '&')
#    ro_key = str.split(data_token[0], '=')
#    ro_secret = str.split(data_token[1], '=')
#    resource_owner_key = ro_key[1]
#    resource_owner_secret = ro_secret[1]
#    resource = [resource_owner_key, resource_owner_secret]
#    return resource
#
#
##Once the resource token is gotten you then enter the prompted website and copy down
##the verifier number and feed it into this funciton along with your resource tokens
##This then gives the app authorization for my Twitter dev account to access the
##desired Twitter account. It returns the desired Twitter account's access token and key
#def twitter_get_access_token(verifier, ro_key, ro_secret):
#    oauth_token = OAuth1Session(client_key=consumer_key,
#                                client_secret=consumer_secret,
#                                resource_owner_key=ro_key,
#                                resource_owner_secret=ro_secret)
#    url = 'https://api.twitter.com/oauth/access_token'
#    data = {"oauth_verifier": verifier}
#   
#    access_token_data = oauth_token.post(url, data=data)
#    print(access_token_data.text)
#    access_token_list = str.split(access_token_data.text, '&')
#    return access_token_list
#
#
##If this is the first time setting up the account then this part of the code runs
##to get authorization and subsequent access tokens for the sales bot to interface
##with a chosen Twitter account
#if access_key == '':
#    #Getting the resource token of my dev account so that another Twitter account can 
#    #authroize my access to it
#    temp = get_resource_token()
#    
#    #This prompts the user to enter the authentication URL for the twitter account 
#    #Once this is entered then a verifier PIN should appear and the user enters it 
#    #in the python console
#    enter_website = 'https://api.twitter.com/oauth/authenticate?oauth_token='+temp[0]
#    print(enter_website)
#    verifier = str(input('enter the verification id'))
#    
#    #Running function to obtain the Twitter account's access token and key that authorized
#    #this code to access 
#    access = twitter_get_access_token(verifier, temp[0], temp[1])
#    access_key = access[0][12:]
#    access_secret = access[1][19:]


#Starting Twitter API session after getting access tokens and access keys

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create API object
api = tweepy.API(auth)

# Create a tweet
#api.update_status("Hello Tweepy")


#Finding the date in which the bot last reported sales.
#Choosing a file to open
root = Tk()
filename = filedialog.askopenfilename()
root.quit()
root.destroy()

while 2 < 6:

    with open(filename) as f:
        lines = f.readlines()
        old_latest_timestamp = pd.Timestamp(lines[0])
    
    #Connecting with OpenSea API to fetch the last sales.
    url = "https://api.opensea.io/api/v1/assets"
    querystring = {"order_by":"sale_date","order_direction":"desc","offset":"0","limit":"50","collection":"cryptopunk-fine-art-portraits"}
    r = requests.request("GET", url, params=querystring)
    h = r.json()
    
    #Analyzing the most recent 50 sales and then sending tweets based on the sale.
    for i in range(len(h['assets'])):
        
        if pd.Timestamp(h['assets'][0]['last_sale']['event_timestamp']) > old_latest_timestamp:
            f = open(filename,"w")
            f.write(h['assets'][0]['last_sale']['event_timestamp'])
            f.close()
        
        if pd.Timestamp(h['assets'][i]['last_sale']['event_timestamp']) <= old_latest_timestamp:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            print('no update')
            break
            
        current_sale = int(h['assets'][i]['last_sale']['total_price'])/1000000000000000000
        
        if h['assets'][i]['num_sales'] == 1:
            print(i)
            print('initial sale')
            print(current_sale)
            link = h['assets'][i]['permalink']
            owner = h['assets'][i]['last_sale']['transaction']['from_account']['user']['username']
            tx_hash = h['assets'][i]['last_sale']['transaction']['transaction_hash']
            title = h['assets'][i]['name']
            eth_price = int(h['assets'][i]['last_sale']['payment_token']['usd_price'][:4])
            if owner is None:
                message1 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + \
                            ')\n \nThank you for the support #NFTCommunity\n \n#FineArtPunks #NFTs #NFTCollectors #unofficialpunks\n \n' + link

                message2 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + \
                            ')\n \nHope you enjoy your #FineArtPunk as much as I enjoyed making it!\n \n#Altpunks #NFTs #NFTCollectors #cryptopunks\n \n' + link
            
                message3 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')\n \
                            \nBe sure to print your #FineArtPunk with the 4k quality download!\n \n#Altpunks #NFTs #NFTCollectors\n \n' + link

                messages = [ message1, message2, message3]
                message = messages[random.randint(0,2)]
                
            else:
                message1 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')!' \
                            '\n \n' + owner + ', Thank you for being a part of the #FineArtPunk family!\n \n#Altpunks #NFTs #NFTCollectors #cryptopunks\n \n' + link
                
                message2 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')!' \
                            '\n \n' + owner + ', We hope you enjoy your #FineArtPunk as much as I enjoyed making it!\n \n#Altpunks #NFTs #NFTCollectors #cryptopunks\n \n' + link
                
                message3 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')!' \
                            '\n \n' + owner + ', there is a 4k high resolution download to show off your #FineArtPunk!\n \n#Altpunks #NFTs #NFTCollectors #cryptopunks\n \n' + link
                
                message4 = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')!' \
                            '\n \n' + owner + ', you snagged a beauty! Thank you for your support!\n \n#Altpunks #NFTs #NFTCollectors #cryptopunks\n \n' + link
                
                messages = [ message1, message2, message3, message4]
                message = messages[random.randint(0,3)]

            
            print(message)
            api.update_status(message)
            time.sleep(800)
        
        if h['assets'][i]['num_sales'] > 1:
            print(i)
            print('secondary sale')
            link = h['assets'][i]['permalink']
            tx_hash = h['assets'][i]['last_sale']['transaction']['transaction_hash']
            title = h['assets'][i]['name']
            eth_price = int(h['assets'][i]['last_sale']['payment_token']['usd_price'][:4])
    
            time.sleep(10)
            url = "https://api.opensea.io/api/v1/events"
            querystring = {"asset_contract_address":"0x495f947276749ce646f68ac8c248420045cb7b5e","collection_slug":"cryptopunk-fine-art-portraits","token_id":str(h['assets'][i]['token_id']),"event_type":"successful","only_opensea":"false","offset":"0","limit":"20"}
            response = requests.request("GET", url, params=querystring)
            g = response.json()
    #        current_sale = int(g['asset_events'][0]['total_price'])/1000000000000000000
            print(current_sale)
            last_sale = int(g['asset_events'][1]['total_price'])/1000000000000000000
            print(last_sale)
            gain = round((current_sale/last_sale)*100 - 100,2)
            if current_sale/last_sale > 1:
                message = title + ' has sold in the secondary market for ' + str(current_sale) + ' ETH ($' + str(round(current_sale*eth_price,2)) + ') from its previous price of ' + str(last_sale) + ' ETH for a ' + str(gain)+ \
                            '%gain!🚀🚀🚀\n \nCongrats to the buyer and seller!\n \n#AltPunks #NFTs #NFTCollectors\n \n' + link
                print(message)
                api.update_status(message)
                time.sleep(800)
            else:
                message = title + ' has sold for ' + str(current_sale) + ' ETH! ($' + str(round(current_sale*eth_price,2)) + ')\n \nThank you for the support #NFTCommunity\n \n#FineArtPunks #NFTs #NFTCollectors #unofficialpunks\n \n' + link
                print(message)
                api.update_status(message)
                time.sleep(800)
                
    time.sleep(600)
            
            
        