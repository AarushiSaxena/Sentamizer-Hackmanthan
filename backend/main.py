import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request, jsonify, render_template
from googletrans import Translator

application = Flask(__name__) #Initialize the flask App

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    class SentimentAnalysis:

       def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.pos='1'
       def DownloadData(self):
        # authenticating
        consumerKey = 'Ubr9uVY2osMRXL5vrNU1uyvty'
        consumerSecret = 'RKwTTQ1bLSTzRUWdKsMV2w238HhFxY41WOlxBktgLpFGpKnntI'
        accessToken = '1481928772308049923-AfTAim4WRASkehoDoxxKTwUXBqQSb0'
        accessTokenSecret = 'O4z9FbXPcdrJkKjGH0796vTG4oKeqy53PVkfxv914Y6gb'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm1 = request.form['experience']
        translater= Translator()
        searchTerm2 = translater.translate(searchTerm1)
        searchTerm=searchTerm2.text
        NoOfTerms = 100

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search_tweets, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        def percentage(part, whole):
           temp = 100 * float(part) / float(whole)
           return format(temp, '.2f')
        def cleanTweet(tweet):
       # Remove Links, Special Characters etc from tweet
          return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            #self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = percentage(positive, NoOfTerms)
        wpositive = percentage(wpositive, NoOfTerms)
        spositive = percentage(spositive, NoOfTerms)
        negative = percentage(negative, NoOfTerms)
        wnegative = percentage(wnegative, NoOfTerms)
        snegative = percentage(snegative, NoOfTerms)
        neutral = percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")
        
        if (polarity == 0):
            self.pos="Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            self.pos="Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            self.pos="Positive"
        elif (polarity > 0.6 and polarity <= 1):
            self.pos="Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            self.pos="Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            self.pos="Negative"
        elif (polarity > -1 and polarity <= -0.6):
            self.pos="Strongly Negative"
        
        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")
        return self.pos
        #self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


     

    # # function to calculate percentage
    

    # def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
    #     labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
    #               'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    #     sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    #     colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
    #     patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    #     plt.legend(patches, labels, loc="best")
    #     plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    #     plt.axis('equal')
    #     plt.tight_layout()
    #     plt.show()
    if __name__== "__main__":
           SentimentAnalysis().DownloadData()

    s1=SentimentAnalysis()
    sent= s1.DownloadData()
    return render_template('index.html', prediction_text='Sentiment:'+ sent)

if __name__ == "__main__":
          application.run(debug=True)