import requests
# import nltk
# nltk.download('punkt')
from textblob import TextBlob

# Certificate error workaround
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
'''import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()'''

def score_sentiment(text):
        '''Extract sentiment (total and average) from  multi-sentence string, sentence by sentence'''
        #Convert string into TextBlob
        blob = TextBlob(text)
        #Print polarity of each sentence
        total_sentiment = 0
        for sentence in blob.sentences:
                total_sentiment += sentence.sentiment.polarity
        avg_sentiment = total_sentiment/len(blob.sentences)
        return avg_sentiment
        # ,total_sentiment
