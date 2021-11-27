from pyspark.sql import SparkSession

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

df_data = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

print("READSTREAM COMPLETE")



query = df_data.writeStream.outputMode("append").format("console").start()
query.awaitTermination()








