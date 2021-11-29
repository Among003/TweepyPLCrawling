from pyspark.sql import SparkSession
from pyspark.sql.streaming import DataStreamWriter, DataStreamReader
from pyspark.sql.types import StructType, StringType , StructField, MapType
from pyspark.sql.functions import from_json, to_json, schema_of_json,get_json_object, col, explode

'''
This program is designed to run on the spark cluster.
It subscribes to messages from kafka and processes them using NLP
'''


# json_schema = StructType([]).add(StructField("created_at",StringType()))\
#     .add(StructField("id_str",StringType()))\
#     .add(StructField("text",StringType()))

j_schema = StructType([StructField("created_at",StringType()),
StructField("id_str",StringType()),
StructField("text",StringType())
])


#MASTER NODE
spark = SparkSession.builder.master("local").appName("twitter").getOrCreate()
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "tweets")\
    .option("startingOffsets","earliest")\
    .load().selectExpr("CAST(value AS STRING)")\
    .select(col("value"))

# json_df = df.select(from_json(col("value").cast("string"),j_schema))
# json_df.printSchema()



print("READSTREAM COMPLETE")

json_df = df.withColumn("jsonData",from_json(col("value"),j_schema)).select("jsonData.*")
json_df.printSchema()
# json_df.show()
# parsed_df = df \
#   .select(explode("parsed_value.text")) \
#   .select("value.*")


# df = df.selectExpr("CAST(value AS STRING)")

# df_data_json = spark.readStream.json(df,schema=json_schema)
# df_data_1 = df.select(get_json_object("value"))
# df_data = df_data_1.select(from_json("value", schema))

# df_data = df.select( \
#         col("key").cast("string"),\
#         from_json(col("value").cast("string"), json_schema))

#TODO NLP 

#TODO

# query = json_df.writeStream.outputMode("append").format("console").option("truncate",False).start()
# query.awaitTermination()

#This writes the data to parquet


# df_data = df.selectExpr("CAST(value AS STRING)")
df_writer = DataStreamWriter(json_df).format("parquet").option("checkpointLocation","/tmp/spark_checkpoints").option("path", "/Users/abraham/Projects/TweepyUtils/processed_data").start()
df_writer.awaitTermination()




