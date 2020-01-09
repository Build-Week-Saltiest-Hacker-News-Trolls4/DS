import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

def score_sentiment(tweet):
        '''Extract sentiment (total and average) from  multi-sentence string, sentence by sentence'''
        words = word_tokenize(tweet)
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in words if w not in stop_words]
        #Convert string into TextBlob
        text = ''.join(filtered_sentence)
        blob = TextBlob(text)
        total_sentiment = 0
        for sentence in blob.sentences:
                total_sentiment += sentence.sentiment.polarity
        avg_sentiment = total_sentiment/len(blob.sentences)
        return avg_sentiment
        # ,total_sentiment
