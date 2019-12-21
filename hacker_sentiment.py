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

    def push_heroku(self):
        # Push to backend

        # Needs df
        df.to_csv('output/top_20.csv', index=False)

        # Put above later
        import sqlite3
        import psycopg2

        # Store elsewhere
        dbname = ''
        user = ''
        password = ''
        host = ''

        pg_conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host)
        pg_curs = pg_conn.cursor()

        # Set table features
        create_top_20_users = '''
            CREATE TABLE top_20_users (
            comment_ID SERIAL PRIMARY KEY,
            author VARCHAR(100),
            comment_Text VARCHAR(1000), # need to figure out how to better set upper limit
            time DATE,
            neg FLOAT,
            pos FLOAT,
            neu FLOAT
        )
        '''
        #pg_curs.execute('DROP TABLE top_20_users')
        #pg_curs.execute("ROLLBACK")

        pg_curs.execute(create_top_20_users)

        # Put above
        import csv

        # Check save time
        start = time.time()

        # Store from saved csv file
        with open('output/???.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip first row of column names
            for row in reader:
                pg_curs.execute('INSERT INTO top_20_users \
                        (%s, %s, %s, %s, %s, %s, %s)', row)
        
        end = time.time()
        print(end - start)



        return 0

                

