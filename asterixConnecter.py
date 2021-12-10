import pandas as pd
import requests
import re 
import json


#READING PARQUET FILE 

df = pd.read_parquet("processed_data")
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

#create_resp = requests.post(asterix_url,data={"statement" : select_tables})

# QUERY TO INSERT TWEETS INTO DB

pattern = re.compile('[\W]+[\s]+[.]+')


list_data = df.to_dict('records')
for data in list_data[0:10]:
    insert_query = 'INSERT INTO twitter_data.ArsenalTweets('
    old_String = data['text']
    new_String = pattern.sub('', old_String)
    data['text'] = new_String
    insert_query += str(data)
    insert_query += ');'
    requests.post(asterix_url,data={'statement':insert_query})





#SELECT QUERY 

select_query = "select * from twitter_data.ArsenalTweets;"

select_resp = requests.post(asterix_url,data={'statement':select_query})

result_dict = json.loads(select_resp.content)

final_dat = df.from_dict(result_dict)

final_dat.to_parquet("newdf.parquet")


