import pandas as pd
import requests
import re 



#READING PARQUET FILE 

df = pd.read_parquet("df.parquet")
asterix_url = "http://localhost:19002/query/service"

df.dropna()
print(df.head())


#QUERY TO CREATE DATAVERSE

create_query = '''
DROP DATAVERSE twitter_data IF EXISTS;
CREATE DATAVERSE twitter_data;
use twitter_data;
CREATE TYPE tweet AS {
id_str : string,
text : string,
sentiment : string,
country : string
};


CREATE DATASET ArsenalTweets(tweet)
        PRIMARY KEY id_str;

'''

select_tables = "select * from Metadata.`Dataverse`;"

create_resp = requests.post(asterix_url,data={"statement" : select_tables})

# QUERY TO INSERT TWEETS INTO DB

pattern = re.compile('[\W]+')

insert_query = 'INSERT INTO ArsenalTweets(['

list_data = df.to_dict('records')
for data in list_data:
    old_String = data['text']
    new_String = pattern.sub('', old_String)
    data['text'] = new_String
    insert_query += str(data)
    insert_query += ','
insert_query = insert_query[:-1]
insert_query += ']);'

print(insert_query)

insert_resp = requests.post(asterix_url,data={'statement':insert_query})



#SELECT QUERY 

select_query = "select * from ArsenalTweets;"

select_resp = requests.post(asterix_url,data={'statement':select_query})