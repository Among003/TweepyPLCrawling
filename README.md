#Start Zookeeper and Kafka

>./kafka-2.8.1-src/bin/zookeeper-server-start.sh config/zookeeper.properties
>./kafka-2.8.1-src/bin/kafka-server-start.sh config/server.properties

#Create Kafka Topic named tweets

./kafka-2.8.1-src/bin/kafka-console-consumer.sh --topic tweets --from-beginning --bootstrap-server localhost:9092

#Install python dependencies
pip3 install -r reqs

#Activate new environment

#Start Tweepy Listener
python3 TweepyPLCrawler.py <hashtag>

#Start spark-submit after adding spark bins to path
  
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 sparkClient.py


#To Visualize data




