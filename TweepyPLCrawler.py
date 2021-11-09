from tweepy import OAuthHandler, Stream, StreamListener 
import json, os, sys
#These are our keys generated with our development account application 

consumer_key="OvtaSdGdSFYG2enOytwNOtdea"
consumer_secret="W4Z8Zki6aQ2hiOE4sv0e6S7BwDHUsJG9nMS1qxzYNCeNCe0b5G"
access_token="4808950815-vd7kZ2tQbHfM6KdIBtrKejEbU4rO3i8usY2mzqR"
access_token_secret="HoiZyEXwrBUIHDKiI3U1VXEZ1uvBgRj6VfTuYE6u44M5X"

#Current simple filter list
#You can have multiple filters/hashtags 
filterList = ['#ARSVIL']
dataDirectory = "JSONData"


def saveToJsonFile(jsonObj):
    print("TODO")



class StreamListener(StreamListener):
    #This is where the main functionality is written.  The listener has 2 functions built in that act 
    #depending on successful tweet pull or failure.
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    if len(sys.argv) < 2:                  #Need to pass in a filter for a hastag
        print("Error, pass in hashtag")    
        quit(1)                           

    if dataDirectory not in os.listdir("."):              #folder to be used to store data.  Everything will be saved locally
        print("Data folder not found, creating 'data directory as '", dataDirectory,"'...")
        os.mkdir(dataDirectory)

    if sys.argv[1] not in os.listdir(dataDirectory + "/"):
        print("Making folder for ",sys.argv[1],"...")
        os.mkdir(dataDirectory + "/" + sys.argv[1]) 

    l = StreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #stream.filter(track=filterList)



#PLANNED FUNCTIONALITY
#1. Passable hashtag through ARGV
#2. Creation of directories based on input hashtag
#3. Saving of Tweets into JSON
#     3.1 Selection of only necessary data from JSON? Or save whole Json file?
#4. Ensuring tweets are original?
