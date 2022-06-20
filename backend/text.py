from textblob import TextBlob
from newspaper import Article

url="https://en.wikipedia.org/wiki/Mathematics"
article= Article(url)

article.download()
article.parse()
article.nlp()

text="hello good morning"
print(text)

blob= TextBlob(text)
sentiment= blob.sentiment.polarity
if(1>=sentiment>=0.6):
    print("Strongly Positive")
    tow="Strongly Positive"
elif(0.6>sentiment>=0.2):
    print("Weakly Positive")
    tow="Weakly Positive"
elif(0.2>sentiment>=-0.2):
    print("Neutral")
    tow="Neutral"
elif(-0.2>sentiment>=-0.6):
    print("Weakly Negative")
    tow="Weakly Negative"
else:
    print("Strongly Negative")
    tow="Strongly Negative"    