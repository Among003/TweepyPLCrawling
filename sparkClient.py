from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import *
from kafka.serializer.abstract import Serializer,Deserializer
from pyspark.sql.avro.functions import from_avro, to_avro

'''
This program is designed to run on the spark cluster.
It subscribes to messages from kafka and processes them using NLP
'''

jsonSchema = open("/Users/abraham/Projects/TweepyUtils/schema","r").read()

#MASTER NODE
spark = SparkSession.builder.master("local").appName("twitter").getOrCreate()
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "tweets")\
    .option("startingOffsets","earliest")\
    .load().select(from_avro("value",jsonSchema))

print("READSTREAM COMPLETE")



query = df.writeStream.outputMode("append").format("console").start()
query.awaitTermination()








