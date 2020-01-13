import html
import json
import re
import requests
import pandas as pd
import sqlite3

from sentiment_model import *
#TODO: max item in DB vs max item on site...
# how to pull the highest comment ID the database contains? 
# Probably requries SQL query.
def remove_html_tags(text):
    '''Removes HTML tags from a string using regular rexpression, returns a string'''
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_new_comments():
    """
    Request latest comments, add usernames and their comments to respective lists, 
    later to databases in separate function

    Returns: 
        comment_ids (list<int>): Filtered comment ids as a list of integers.
        usernames (list<str>): Comment usernames as a list of strings.
        filtered_comments (list<str>): Filtered post ids as a list of strings.

    """
    max_item_id = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty').json()
    comment_ids = [] 
    usernames = [] 
    filtered_comments = []
    # Accessing file
    txt_file = open("latest_comment_id.txt","r")
    # Assumes the file contains a single line
    latest_comment_id = int(txt_file.read())
    # Erase old value
    txt_file.close()
    # Write new latest_comment_id value
    txt_file = open("latest_comment_id.txt","w")
    txt_file.write(f'{max_item_id}')
    txt_file.close()

    

    # Count down from most recent comment id until range limit is reached

    for item_id in range(latest_comment_id+1, max_item_id): 
            post = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json').json()
            
            # Get comment text and commenter
            if (post['type'] == 'comment'):
              comment_id = post.get('id')
              user = post.get('by')
              text = post.get('text') 
              
              # Text==null if post was deleted
              if text:
                  filtered_comments.append(text)
                  comment_ids.append(item_id)
                  usernames.append(user)       
 
    df = pd.DataFrame(list(zip(comment_ids, usernames, filtered_comments)), columns=['comment_ID', 'username', 'comment'])
    df['comment']=df['comment'].apply(str)
    df['comment'] = df['comment'].apply(lambda x: remove_html_tags(x))
    df['comment'] = df['comment'].apply(lambda x: html.unescape(x))
    df['sentiment'] = df['comment'].apply(lambda x: score_sentiment(x))
    return df

def update_user_scores(new_comments):
    #Check to see if sqlite3 db exists, if not create it
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL,
        avg_score REAL NOT NULL,
        num_comments INTEGER NOT NULL,
        saltiest_comment BLOB NOT NULL,
        saltiest_comment_sentiment REAL NOT NULL,
        saltiest_comment_id INTEGER NOT NULL)
        ''')
    #Split new_comments into existing_users (already in db) and new_users (not in db yet)

    #For existing users recalculate avg_score, num_comments, saltiest_comment, saltiest_comment_id
    # Check to see if sqlite3 db exists so, connect, if not create it
    
    # For existing_users recalculate avg_score, num_comments, saltiest_comment, saltiest_comment_sentiment, saltiest_comment_id
    # For new users, append (for now, there is a stretch annotated below)

    col = {'user':1, 'avg_score':2, 'num_comments':3, 'saltiest_comment':4, 'saltiest_comment_id':5}
    
    for ind in new_comments.index:
        this_user = new_comments['username'][ind]
        
        cursor.execute(f'''
                        SELECT avg_score, num_comments, saltiest_comment, saltiest_comment_sentiment, saltiest_comment_id
                        FROM user_scores
                        WHERE user = "{this_user}" 
                        ''')
        
       
        # Case: Existing user
        this_user_stats = cursor.fetchall()
        if this_user_stats != []:
            # Update avg_score
            avg_score = this_user_stats[0][0]
            num_comments = this_user_stats[0][1]
            this_comment_sentiment = new_comments['sentiment'][ind]

            new_avg_score = (avg_score * num_comments + this_comment_sentiment) / (num_comments + 1)

            # Update num_comments
            new_num_comments = num_comments + 1

            cursor.execute(f'''
                            UPDATE user_scores
                            SET avg_score = {new_avg_score},
                                num_comments = {new_num_comments}
                            WHERE user = "{this_user}"
                            ''')

            # Update saltiest_comment and saltiest_comment_id if needed
            if this_comment_sentiment < this_user_stats[0][3]:
                cursor.execute(f'''
                            UPDATE user_scores
                            SET saltiest_comment = "{new_comments['comment'][ind].replace('"',"'")}",
                                saltiest_comment_sentiment = {new_comments['sentiment'][ind]},
                                saltiest_comment_id = {new_comments['comment_ID'][ind]}
                            WHERE user = "{this_user}"
                            ''')
            conn.commit()
        # Case: New user
        else:
            # Append user to db
            cursor.execute(f'''
                            INSERT INTO user_scores (user, avg_score, num_comments, 
                                                    saltiest_comment, saltiest_comment_sentiment, saltiest_comment_id)
                            VALUES("{this_user}", {new_comments['sentiment'][ind]}, 1, 
                                    "{new_comments['comment'][ind].replace('"',"'")}", {new_comments['sentiment'][ind]}, 
                                    {new_comments['comment_ID'][ind]})
                            ''')
            conn.commit()
            
            # Get the last 30 posts by this new user, to ensure reasonable avg_sentiment.  
            historic_posts = get_user_posts(this_user, limit=30)
            update_user_scores(historic_posts)  

    df = pd.read_sql_query('SELECT * FROM user_scores', conn)
    # df = pd.DataFrame(query, columns=['id', 'user', 'avg_score', 'num_comments',
    #                                  'saltiest_comment', 'saltiest_comment_sentiment',
    #                                  'saltiest comment_id'])
    df = df.set_index('id')
    # df['avg_score'] = scale_sentiments(df['avg_score'])
    return df.sort_values(by='avg_score', ascending=False)
    # return df sorted by saltiness
 


def get_user_posts(username, filter_posts="comment", limit=100):
    """ 
    Filter user posts by type of item.
  
    Current implimentation only works for 'comment'
  
    Parameters: 
    username (str): Username for which to return posts.
    filter_posts (str): Type of posts to return ("job", "story", "comment", "poll", or "pollopt").
    limit (int): The maximum number of posts to return
  
    Returns: 
    Pandas df['comment_ID', 'username', 'comment', 'sentiment']
  
    """
    # TODO: currently only supports 'comment' type
    # TODO: handle case where user posts so many stories that it causes timeout
    # TODO: Currently ingests 'title' of 'story', decide whether that should stay

    response = requests.get(f'https://hacker-news.firebaseio.com/v0/user/{username}.json')
    post_ids = response.json()["submitted"]
    
    filtered_post_ids = []
    filtered_posts = []
   
    for post_id in post_ids:
        # This should be a function extract_text()
        # Post is a python dict
        post = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{post_id}.json').json()
        if (post['type'] == filter_posts):
            text = post.get('text')   
            
            # text==null if post was deleted
            if text:
                filtered_posts.append(text)
                filtered_post_ids.append(post_id)
        elif (post['type'] == 'story'):
            text = post.get('title')

            if text:
                filtered_posts.append(text)
                filtered_post_ids.append(post_id)

        # Checks whether the specified limit has been reached
        if len(filtered_posts) == limit:
            break
    
    usernames = [username] * len(filtered_posts)

    # Create and refactor df
    df = pd.DataFrame(list(zip(filtered_post_ids, usernames, filtered_posts)), columns=['comment_ID', 'username', 'comment'])
    df['comment']=df['comment'].apply(str)
    df['comment'] = df['comment'].apply(lambda x: remove_html_tags(x))
    df['comment'] = df['comment'].apply(lambda x: html.unescape(x))
    df['sentiment'] = df['comment'].apply(lambda x: score_sentiment(x))
    return df
