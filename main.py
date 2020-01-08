# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User
from heroku_pass_off import push_heroku

# Debug Start: Delete this
hacker_access.get_new_comments()
# Debug End: Delete this

users_usernames = hacker_access.get_user_list()
observations = []

for username in users_usernames[0:20]:

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



