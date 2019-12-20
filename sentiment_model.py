import requests
import nltk
nltk.download('punkt')
from textblob import TextBlob


def score_sentiment(text):
        '''Extract sentiment (total and average) from  multi-sentence string, sentence by sentence'''
        #Convert string into TextBlob
        blob = TextBlob(text)
        #Print polarity of each sentence
        total_sentiment = 0
        for sentence in blob.sentences:
                total_sentiment += sentence.sentiment.polarity
        avg_sentiment = total_sentiment/len(blob.sentences)
        return total_sentiment, avg_sentiment

<<<<<<< HEAD
        # my comment > your comment
=======
#Test commit (DeleteME)
>>>>>>> 15be4bdabfd9c0942274536d9b703e61e278ca8f
