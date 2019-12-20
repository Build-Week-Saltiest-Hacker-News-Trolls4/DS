import pandas as pd
from datetime import datetime
from .sentiment_model import score_sentiment
from .get_user_posts import get_user_posts


class User():
    def __init__(self, username):
        self.username = username
        cols = ['comment_id', 'text', 'sentiment']
        scored_comments = pd.DataFrame(columns=cols)
        update_sentiment(self.username)
        last_update = datetime.now()
        latest_comment_id = scored_comments.tail(1)['comment_id']
        mean_sentiment = 0
        

    def update_sentiment(self):
        # Load new comments into df
        new_comments_df = get_new_comments(self.username, self.latest_comment_id)

        # Score new comments
        new_comments_df['sentiment'] = score_sentiment(new_comments_df['text'])
        
        # Append to scored_comments
        self.scored_comments.Append(new_comments_df)
        self.latest_comment_id = self.scored_comments.tail(1)['comment_id']
        self.mean_sentiment = self.scored_comments['sentiment'].mean()

    def get_new_comments(username, last_loaded_comment=0):
        """Returns pandas dataframe {'comment_id', 'text'} with id > last_loaded_comment"""
        # TODO: Implement

        # Dummy return
        dummy_df = pd.DataFrame([[0,'dummy text', 0]], columns=self.cols)
        return dummy_df


    def get_saltiest_comment(self):
        #return comment with min sentiment
        # TODO: Implement

        # Dummy return
        dummy_comment = [0, 'dummy saltiest text', 0]
        return dummy_comment   

    def push_heroku():


