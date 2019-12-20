# Main application logic goes here
import hacker_access
import pandas as pd
from hacker_user import User

top_users_usernames = hacker_access.get_user_list()

cols = ['rank', 'score', 'username', 
        'saltiest_comment_text', 'saltiest_comment_id']
top_users_report = pd.DataFrame(columns=cols)

# Build top n users table
for username in top_users_usernames:
    user = User(username)
    user.update_sentiment() # Consider calling as part of __init__

    mean_sentiment = user.mean_sentiment
    saltiest_comment = user.get_saltiest_comment()
    saltiest_comment_text = 



