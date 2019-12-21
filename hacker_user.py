import pandas as pd
from datetime import datetime
from sentiment_model import score_sentiment
from hacker_access import get_user_posts

class User():


    def __init__(self, username):
        self.username = username
        cols = ['comment_id', 'text', 'sentiment']
        self.scored_comments = pd.DataFrame(columns=cols)
        print(f'Debug: initialized {username} database') # Debug use. delete.
        self.get_sentiment()
        self.last_update = datetime.now()
        self.latest_comment_id = self.scored_comments.tail(1)['comment_id']
        self.mean_sentiment = 0
        print(f'Debug: initialization of {username} completed.') # Debug use. delete.

    def get_new_comments(self, username, last_loaded_comment=0):
        """Returns pandas dataframe {'comment_id', 'text'} with id > last_loaded_comment"""
        ids, posts = get_user_posts(username, limit=20)
        comments_df = pd.DataFrame(list(zip(ids, posts)))
        
        # Dummy return
        # dummy_df = pd.DataFrame([[0,'dummy text', 0]], columns=self.cols)
        return comments_df

    def get_sentiment(self):
        '''Gets sentiment value from scratch'''
        comments = get_user_posts(self.username, limit=20)
        self.scored_comments['comment_id'], self.scored_comments['text'] = comments
        self.scored_comments['sentiment'] = score_sentiment(self.scored_comments['text'][0])
        self.mean_sentiment = self.scored_comments['sentiment'].mean()

    def update_sentiment(self):
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
        # TODO: Implement, builds off get_new_comments

        # Dummy return values
        id = 0
        text = 'dummy saltiest text'
        score = 0.0

        slatiest_comment = {'id' : id, 'text' : text, 'score' : score}
        return slatiest_comment