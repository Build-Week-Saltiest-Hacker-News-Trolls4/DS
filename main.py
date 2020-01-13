# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User
from heroku_pass_off import push_heroku

# users_usernames = hacker_access.get_user_list()
df_by_comments = hacker_access.get_new_comments()
df_by_users = hacker_access.update_user_scores(df_by_comments)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']
users_report = df_by_users.rename(columns={"avg_score": "score", "user": "username",
                                "saltiest_comment": "saltiest_comment_text"})
users_report.drop(['num_comments', 'saltiest_comment_sentiment'], axis='columns', inplace=True)
users_report = users_report.sort_values(by=['score'], ascending=False)
users_report = users_report.reset_index(drop=True)
top_20_table = users_report.head(20)

push_heroku(top_20_table)