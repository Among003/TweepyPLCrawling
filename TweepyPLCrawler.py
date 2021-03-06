from tweepy import Stream
import json, os, sys 
from kafka import KafkaProducer
from pyspark.sql.avro.functions import *

#These are our keys generated with our development account application 


consumer_key="OvtaSdGdSFYG2enOytwNOtdea"
consumer_secret="W4Z8Zki6aQ2hiOE4sv0e6S7BwDHUsJG9nMS1qxzYNCeNCe0b5G"
access_token="4808950815-vd7kZ2tQbHfM6KdIBtrKejEbU4rO3i8usY2mzqR"
access_token_secret="HoiZyEXwrBUIHDKiI3U1VXEZ1uvBgRj6VfTuYE6u44M5X"

#Current simple filter list
#You can have multiple filters/hashtags.  Add some default ones here, or pass it in through argv 
filterList = []
dataDirectory = "JSONData"

prod = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'tweets'

# schema = avro.schema.parse(open("schema").read())

def saveToJsonFile(jsonObj):
    outfile = open(dataDirectory + "/" + sys.argv[1] + "/" +jsonObj.get("id_str") + ".json", 'w')
    print("Saving tweet: ", jsonObj.get("id_str"))
    json.dump(jsonObj, outfile, indent = 5)
    prod.send(topic_name, jsonObj.encode('utf-8'))
    outfile.close()


class StreamListener(Stream):
    #This is where the main functionality is written.  The listener has 2 functions built in that act 
    #depending on successful tweet pull or failure.
    def on_data(self, data):
        dataJson = json.loads(data)
        try:
            if dataJson['lang'] == 'en':
                stream_json = {}
                stream_json["created_at"] = dataJson["created_at"]
                stream_json["id_str"] = dataJson["id_str"]
                stream_json["text"] = dataJson["text"]
                stream_json["coordinates"] = dataJson["coordinates"]
                stream_json["sentiment"] = "0"
            print("Saving tweet: ", dataJson.get("id_str"))
            #saveToJsonFile(dataJson)
            prod.send(topic_name,json.dumps(stream_json).encode('utf-8'))
        except:
            print("nope")
            # prod.send(topic_name, bytesData)
        else:
            print("Ignoring non-english tweet..") 
        return True
        
    def on_connection_error(self):
        self.disconnect()
        print("Error:Could not connect!")
        
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
    
    filterList.append(sys.argv[1])
    # l = StreamListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    stream = StreamListener(consumer_key=consumer_key, consumer_secret=consumer_secret,\
        access_token=access_token,access_token_secret=access_token_secret)
    stream.filter(track=filterList)



#PLANNED FUNCTIONALITY
#1. Passable hashtag through ARGV DONE
#2. Creation of directories based on input hashtag  DONE
#3. Saving of Tweets into JSON  DONE
#     3.1 Selection of only necessary data from JSON? Or save whole Json file? ???? TODO???
#4. Ensuring tweets are original?  TODO
