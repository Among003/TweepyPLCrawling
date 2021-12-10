import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_parquet('df.parquet')
countryList = df.country.unique()
countryList = [ x.strip() for x in countryList ]

countries = []
positiveTweets = []
negativeTweets = []

#sentimentCount = df['country'].value_counts()
for country in countryList:
    tempDF = df.loc[df['country'] == country]
    
    positiveTweetDF = tempDF.loc[tempDF['sentiment'] == "1"]
    positiveTweetCount = len(positiveTweetDF.index)

    pd.set_option('display.max_columns', None)
    print(positiveTweetDF.head())


    negativeTweetDF = tempDF.loc[tempDF['sentiment'] == "-1"]
    negativeTweetCount = len(negativeTweetDF.index)
    
    #print("positive ", positiveTweetCount)
    #print("negative ", negativeTweetCount) 
    
    if (positiveTweetCount > 1000 or negativeTweetCount > 1000):
        countries.append(country)
        positiveTweets.append(positiveTweetCount)
        negativeTweets.append(negativeTweetCount)              
    #positiveTweets.append((tempDF.loc[tempDF['sentiment'] == 1]).columns[0].count)
    #negativeTweets.append((tempDF.loc[tempDF['sentiment'] == -1]).columns[0].count)
    #print(tempDF)

#print(len(countries),  '\n') 
#print((positiveTweets), '\n', (negativeTweets))



x = np.arange(len(countries))
width = 0.40

figure, a = plt.subplots()
bar1 = a.bar(x - width/2, positiveTweets, width, label='Positive Tweets')
bar2 = a.bar(x + width/2, negativeTweets, width, label='Negative Tweets')

a.set_ylabel("Total Sentiment Counts")
a.set_title("Sentiments for Arsenal (against Everton)")
a.set_xticks(x,countries)
a.legend()
a.bar_label(bar1, padding = 0)
a.bar_label(bar2, padding = 0)

figure.tight_layout()
plt.show()

#print(sentimentCount)


