import json, os, sys
from kafka import KafkaConsumer
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext


#consumer = KafkaConsumer('tweets')   #This is working, but we want spark streaming to process datastreams
'''
sc = SparkContext(appName="tweets")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 60)      #throws error
tweets = ssc.socketTextStream("localhost", 9092)
'''
spark = SparkSession.builder.master("local").appName("twitter").getOrCreate()
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "tweets").load() #throwing error

while 1:
    query = df.writeStream.outputMode("append").format("console").start()
    query.awaitTermination()
    print("PRINTING DF" + query.latest())

#tweets = tweets.flatMap(lambda line: line.split("\n")) #Should split tweets as they come in, then we push to mongo db for now

#for msg in consumer:
#        print (msg)



