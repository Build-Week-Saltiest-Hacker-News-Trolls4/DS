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

#Test commit (DeleteME)
