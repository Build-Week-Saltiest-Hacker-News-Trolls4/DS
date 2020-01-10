# from decouple import config
import json
import requests

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
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
        # blob = TextBlob(text)
        # total_sentiment = 0
        api_key = "AIzaSyAnwbBNaqHVuM82djR3-nybIezDsBu-X8Q"
        url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
            '?key=' + api_key)
        data_dict = {
            'comment': {'text': text},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = requests.post(url=url, data=json.dumps(data_dict)) 
        response_dict = json.loads(response.content) 
        avg_sentiment = response_dict["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        # for sentence in blob.sentences:
        #         total_sentiment += sentence.sentiment.polarity
        # avg_sentiment = total_sentiment/len(blob.sentences)
        return avg_sentiment
        # ,total_sentiment

def scale_sentiments(sentiments):
    '''
    Use QuantileTransformer to convert sentiment score to value between 0 and 100
    input: initial Sentiment Score pandas Series
    returns: scaled Sentiment Score pandas Series
    '''
    scaler = QuantileTransformer()
    scaler.fit_transform(sentiments)
    sentiments = [score*100 for score in sentiments]
    return pd.Series(sentiments)