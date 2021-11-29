from pyspark.sql import SparkSession
from pyspark.sql.streaming import DataStreamWriter
'''
This program is designed to run on the spark cluster.
It subscribes to messages from kafka and processes them using NLP
'''



#MASTER NODE
spark = SparkSession.builder.master("local").appName("twitter").getOrCreate()
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "tweets")\
    .option("startingOffsets","earliest")\
    .load()

df_data = df.selectExpr("CAST(value AS STRING)")

print("READSTREAM COMPLETE")

#TODO NLP 

#TODO


#query = df_data.writeStream.outputMode("append").format("console").start()
#query.awaitTermination()
#This writes the data to parquet

df_writer = DataStreamWriter(df_data).format("parquet").option("checkpointLocation","/tmp/spark_checkpoints").option("path", "/Users/abraham/Projects/TweepyUtils/processed_data").start()
df_writer.awaitTermination()




