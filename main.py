# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User

users_usernames = hacker_access.get_user_list()

observations = []

for username in users_usernames:

    print('Loading user: ', username) # Debug use only, delete.

    user = User(username)
    user.update_sentiment() # Consider calling as part of __init__

    mean_sentiment = user.mean_sentiment
    saltiest_comment = user.get_saltiest_comment()

    user_report = [mean_sentiment, username, saltiest_comment['text'], saltiest_comment['id']]
    observations.append(user_report)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']

users_report = pd.DataFrame(observations, columns=headers)

print(users_report) # Debug use only, delete.



