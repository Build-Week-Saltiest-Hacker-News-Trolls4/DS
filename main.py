# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User
from heroku_pass_off import push_heroku

users_usernames = hacker_access.get_user_list() # [:5] if for dubug use only
# print(users_usernames[0:10])
observations = []

for username in users_usernames[0:20]:

    print('Loading user: ', username) # Debug use only, delete.

    user = User(username)

    mean_sentiment = user.mean_sentiment
    print(f'main mean:{mean_sentiment}')
    saltiest_comment = user.get_saltiest_comment()
    print(f'saltiest:{saltiest_comment}')

    user_report = [mean_sentiment, username, saltiest_comment['text'], saltiest_comment['id']]
    observations.append(user_report)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']

users_report = pd.DataFrame(observations, columns=headers)
users_report = users_report.sort_values(by=['score'])
users_report.reindex()
top_20_table = users_report.head(20)

print(f'passing to heroku: \n{top_20_table}')
# push_heroku(top_20_table)



