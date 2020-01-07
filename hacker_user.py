import pandas as pd
from datetime import datetime
from sentiment_model import score_sentiment
from hacker_access import get_user_posts

class User():


    def __init__(self, username):
        self.username = username
        self.mean_sentiment = 0
        cols = ['comment_id', 'text', 'sentiment']
        self.scored_comments = pd.DataFrame(columns=cols)
        self.get_sentiment()
        self.last_update = datetime.now()
        self.latest_comment_id = self.scored_comments.tail(1)['comment_id']

    def get_new_comments(self, username, last_loaded_comment=0):
        """Returns pandas dataframe {'comment_id', 'text'} with id > last_loaded_comment"""
        ids, posts = get_user_posts(username, limit=20)
        comments_df = pd.DataFrame(list(zip(ids, posts)))
        
        return comments_df

    def get_sentiment(self):
        '''Gets sentiment value from scratch'''
        comments = get_user_posts(self.username, limit=20)
        self.scored_comments['comment_id'], self.scored_comments['text'] = comments
        self.scored_comments['sentiment'] = self.scored_comments['text'].apply(lambda row: score_sentiment(row))
        self.mean_sentiment = self.scored_comments['sentiment'].mean()

    def update_sentiment(self):
        '''Loads only new comments. Depends on: get_new_comments() and score_comments()'''
        # Load new comments into "Scored comments" DataFrame
        new_comments_df = self.get_new_comments(self.username)

        # Score new comments
        new_comments_df['sentiment'] = score_sentiment(new_comments_df['text'])
        
        # Append to scored_comments
        self.scored_comments.Append(new_comments_df)
        self.latest_comment_id = self.scored_comments.tail(1)['comment_id']
        self.mean_sentiment = self.scored_comments['sentiment'].mean()

    def get_saltiest_comment(self):
        """return comment with min sentiment as a dictionary"""
        saltiest_comment = self.scored_comments[self.scored_comments.sentiment == self.scored_comments.sentiment.min()]
       
        return saltiest_comment