# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User

top_users_usernames = hacker_access.get_user_list()

observations = []

# Build top n users table
# Debug: takes forever
# for username in top_users_usernames:

for username in top_users_usernames:

    # Debug
    print('Loading user: ', username)

    user = User(username)
    user.update_sentiment() # Consider calling as part of __init__

    mean_sentiment = user.mean_sentiment
    saltiest_comment = user.get_saltiest_comment()

    user_report = [mean_sentiment, username, saltiest_comment['text'], saltiest_comment['id']]
    observations.append(user_report)

headers = ['score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']

top_users_report = pd.DataFrame(observations, columns=headers)

print('works till here')
print(top_users_report)



