from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
from newspaper import Article
from googletrans import Translator

application = Flask(__name__) #Initialize the flask App
@application.route('/')
def home():
    return render_template('base.html')

@application.route('/predict', methods=['POST','GET'])
def predict():
    from textblob import TextBlob
    from newspaper import Article

    url="https://en.wikipedia.org/wiki/Mathematics"
    article= Article(url)

    article.download()
    article.parse()
    article.nlp()

    text1=request.form['exper']
    translater= Translator()
    text2= translater.translate(text1)
    text=text2.text
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
    return render_template('base.html', prediction_tex='Sentiment:'+tow)

if __name__ == "__main__":
          application.run(port=5001,debug=True)