# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User
from heroku_pass_off import push_heroku

df_by_comments = hacker_access.get_posts_and_users()
# df_by_users = hacker_access.update(df_by_comments)
observations = []

# df.sort_values('comment_id')

for username in df_by_comments.sort_values(by='sentiment', ascending=False)['username']:

    print('Loading user: ', username) # Debug use only, delete.

    user = User(username)

    mean_sentiment = user.mean_sentiment
    saltiest_comment = user.get_saltiest_comment()

    saltiest_comment_text = saltiest_comment['text'].to_string(index=False)
    saltiest_comment_id = saltiest_comment['comment_id'].to_string(index=False)

    user_report = [mean_sentiment, username, saltiest_comment_text, saltiest_comment_id]
    observations.append(user_report)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']

users_report = pd.DataFrame(observations, columns=headers)
users_report = users_report.sort_values(by=['score'])
users_report = users_report.reset_index(drop=True)
top_20_table = users_report.head(20)

print(f'passing to heroku: \n{top_20_table}')
push_heroku(top_20_table)



