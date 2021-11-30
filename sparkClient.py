from pyspark.sql import SparkSession
from pyspark.sql.streaming import DataStreamWriter, DataStreamReader
from pyspark.sql.types import StructType, StringType , StructField, MapType, StringType
from pyspark.sql.functions import from_json, to_json, schema_of_json,get_json_object, col, explode, when, UserDefinedFunction
import classifier


'''
This program is designed to run on the spark cluster.
It subscribes to messages from kafka and processes them using NLP
'''


# json_schema = StructType([]).add(StructField("created_at",StringType()))\
#     .add(StructField("id_str",StringType()))\
#     .add(StructField("text",StringType()))

j_schema = StructType([StructField("created_at",StringType()),
StructField("id_str",StringType()),
StructField("text",StringType()),
StructField("sentiment", StringType()),
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

print("READSTREAM COMPLETE")

json_df = df.withColumn("jsonData",from_json(col("value"),j_schema)).select("jsonData.*")
json_df.printSchema()


# def process(x):
#     print(x.text)
#     print("TEST")
#     custom_tokens = classifier.remove_noise(classifier.word_tokenize(x.text))
#     x['sentiment'] = classifier.classifyTokens(custom_tokens)
#     return x

def classify(tweet):
    #print(type(tweet))
    custom_tokens = classifier.remove_noise(classifier.word_tokenize(str(tweet)))
    rating = classifier.NBclassifier.classify(dict([token, True] for token in custom_tokens))
    #print(tweet, rating)
    if (rating == "Positive"):
        return "1"
    return "-1"

# def giveSentimentRating(data):
#     return data.foreach(process)
    #tokenizedWords = tokenize()

# json_df2 = json_df.foreach(process)

#json_df2 = json_df.withColumn("sentiment", when (classify(json_df.text) == "Positve",str(giveSentimentRating(json_df))).otherwise(json_df.sentiment))

udf = UserDefinedFunction(lambda x: str(classify(x)), StringType())

json_df2=json_df.withColumn("sentiment", udf((json_df.text))).select("id_str","text","sentiment").distinct()

#TODO NLP 
# words = data.flatMap(tokenize)
# words = data.removeNoise(words)
# print words.take(10)
#TODO

#query = json_df.writeStream.foreach(process).start()
query = json_df2.writeStream.outputMode("append").format("console").option("truncate",False).start()
query.awaitTermination()

#This writes the data to parquet


# df_data = df.selectExpr("CAST(value AS STRING)")
#df_writer = DataStreamWriter(json_df).format("parquet").option("checkpointLocation","/tmp/spark_checkpoints").option("path", "/Users/abraham/Projects/TweepyUtils/processed_data").start()
#df_writer.awaitTermination()




#We can use join
#We can use continous