# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User
from heroku_pass_off import push_heroku

# users_usernames = hacker_access.get_user_list()
print("db: 1")
df_by_comments = hacker_access.get_new_comments()
print(f"db: 2 \n {df_by_comments}")
df_by_users = hacker_access.update_user_scores(df_by_comments)
# observations = []

# df.sort_values('comment_id')

# for username in users_usernames[0:20]:

#     print('Loading user: ', username) # Debug use only, delete.

#     user = User(username)

#     mean_sentiment = user.mean_sentiment
#     saltiest_comment = user.get_saltiest_comment()

#     saltiest_comment_text = saltiest_comment['text'].to_string(index=False)
#     saltiest_comment_id = saltiest_comment['comment_id'].to_string(index=False)

#     user_report = [mean_sentiment, username, saltiest_comment_text, saltiest_comment_id]
#     observations.append(user_report)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']
print(df_by_users)
users_report = df_by_users.rename(columns={"avg_score": "score", "user": "username",
                                "saltiest_comment": "saltiest_comment_text"})
print(users_report)
users_report.drop(['num_comments', 'saltiest_comment_sentiment'], axis='columns', inplace=True)
users_report = users_report.sort_values(by=['score'], ascending=False)
users_report = users_report.reset_index(drop=True)
top_20_table = users_report.head(20)

print(f'passing to heroku: \n{top_20_table}')
# push_heroku(top_20_table)