# To Visualize our preprocessed data from df.parquet
## To Visualize data

> python3 visualize.py

# To collect and process new data from Twitter and store to AsterixDB

## Start Zookeeper and Kafka

> ./kafka-2.8.1-src/bin/zookeeper-server-start.sh config/zookeeper.properties

> ./kafka-2.8.1-src/bin/kafka-server-start.sh config/server.properties

## Create Kafka Topic named tweets

> ./kafka-2.8.1-src/bin/kafka-console-consumer.sh --topic tweets --from-beginning --bootstrap-server localhost:9092

## Install python dependencies
> pip3 install -r reqs

## Activate new environment
> source /path/to/bin/activate
## Add spark bins to path
> export SPARK_HOME="/path/to/spark"

## Start Tweepy Listener
> python3 TweepyPLCrawler.py arsenal

## Start spark-submit 
  
> spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 sparkClient.py

## Start Asterix DB

> ./apache-asterixdb-0.9.6/opt/local/bin/start-sample-cluster.sh 

## After collecting tweets, start

> python3 asterixConnecter.py





