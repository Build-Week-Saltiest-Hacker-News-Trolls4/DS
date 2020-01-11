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
    print("db: a")
    # Accessing file
    txt_file = open("latest_comment_id.txt","r")
    # Assumes the file contains a single line
    latest_comment_id = int(txt_file.read())
    # Erase old value
    txt_file.close()
    print("db: b")
    # Write new latest_comment_id value
    txt_file = open("latest_comment_id.txt","w")
    txt_file.write(f'{max_item_id}')
    txt_file.close()
    print("db: c")

    

    # Count down from most recent comment id until range limit is reached

    for item_id in range(latest_comment_id+1, max_item_id): 
            print(f"db: d- {item_id}")
            post = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json').json()
            
            #Get comment text and commenter
            if (post['type'] == 'comment'):
              comment_id = post.get('id')
              user = post.get('by')
              text = post.get('text') 
              
              #Text==null if post was deleted
              if text:
                  filtered_comments.append(text)
                  comment_ids.append(item_id)
                  usernames.append(user)
            # print(user, item_id, text)        
 
    df = pd.DataFrame(list(zip(comment_ids, usernames, filtered_comments)), columns=['comment_ID', 'username', 'comment'])
    df['comment']=df['comment'].apply(str)
    df['comment'] = df['comment'].apply(lambda x: remove_html_tags(x))
    df['comment'] = df['comment'].apply(lambda x: html.unescape(x))
    df['sentiment'] = df['comment'].apply(lambda x: score_sentiment(x))
    for i in range(len(df['comment'])):
        print(df['comment'][i])
    return df

def update_user_scores(new_comments):
    #Check to see if sqlite3 db exists, if not create it
    print(f"db: update_user_scores ->\n {new_comments}")

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
        print(f"db: update_user_scores -> {new_comments['username'][ind]}")
        this_user = new_comments['username'][ind]
        
        cursor.execute(f'''
                        SELECT avg_score, num_comments, saltiest_comment, saltiest_comment_sentiment, saltiest_comment_id
                        FROM user_scores
                        WHERE user = "{this_user}" 
                        ''')
        
       
        # Case: Existing user
        if cursor.rowcount > 0:
            this_user_stats = cursor.fetchall()
            
            # Update avg_score
            avg_score = this_user_stats[col['avg_score']]
            num_comments = this_user_stats[col['num_comments']]
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
            if this_comment_sentiment < this_user_stats[col['saltiest_comment_sentiment']]:
                cursor.execute(f'''
                            UPDATE user_scores
                            SET saltiest_comment = {new_comments['comment'][ind].replace('"',"'")},
                                saltiest_comment_sentiment = {new_comments['sentiment'][ind]},
                                saltiest_comment_id = {new_comments['comment_ID'][ind]}
                            WHERE user = "{this_user}""
                            ''')

        # Case: New user
        else:
            # append user to db
            print(f"About to try appending:\n {this_user, new_comments['sentiment'][ind], 1, new_comments['comment'][ind], new_comments['sentiment'][ind], new_comments['comment_ID'][ind]}")
            cursor.execute(f'''
                            INSERT INTO user_scores (user, avg_score, num_comments, 
                                                    saltiest_comment, saltiest_comment_sentiment, saltiest_comment_id)
                            VALUES("{this_user}", {new_comments['sentiment'][ind]}, 1, 
                                    "{new_comments['comment'][ind].replace('"',"'")}", {new_comments['sentiment'][ind]}, 
                                    {new_comments['comment_ID'][ind]})
                            ''')
        conn.commit()    
    # Stretch
    # For new_users get_last_30_comments and include in calculations
    df = pd.read_sql_query('SELECT * FROM user_scores', conn)
    # df = pd.DataFrame(query, columns=['id', 'user', 'avg_score', 'num_comments',
    #                                  'saltiest_comment', 'saltiest_comment_sentiment',
    #                                  'saltiest comment_id'])
    df = df.set_index('id')
    # df['avg_score'] = scale_sentiments(df['avg_score'])
    print("------\n", df)
    print("type: ", type(df))
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
    filtered_post_ids (list<int>): Filtered post ids as a list of integers.
    filtered_posts (list<str>): Filtered post ids as a list of strings.
  
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

    return filtered_post_ids, filtered_posts

def get_user_list(criteria='top100'):
    if criteria=='top100':
        users_string = '''tptacek	sd
                        2.	jacquesm	sd
                        3.	patio11	sd
                        4.	danso	sd
                        5.	ingve	sd
                        6.	ColinWright	sd
                        7.	rayiner	sd
                        8.	ChuckMcM	sd
                        9.	rbanffy	sd
                        10.	prostoalex	sd
                        11. Animats	79907
                        12.	mikeash	74346
                        13.	edw519	73178
                        14.	jgrahamc	71990
                        15.	JumpCrisscross	71683
                        16.	dragonwriter	68034
                        17.	TeMPOraL	67554
                        18.	steveklabnik	67203
                        19.	uptown	66695
                        20.	shawndumas	66398
                        21.	nostrademons	63728
                        22.	luu	63128
                        23.	jerf	62527
                        24.	anigbrowl	61255
                        25.	coldtea	60694
                        26.	llambda	58088
                        27.	fogus	56893
                        28.	Tomte	55753
                        29.	jrockway	54930
                        30.	jseliger	54593
                        31.	pjc50	53735
                        32.	aaronbrethorst	53634
                        33.	cperciva	52499
                        34.	adamnemecek	52486
                        35.	davidw	52403
                        36.	pseudolus	52078
                        37.	DanBC	51403
                        38.	lelf	51133
                        39.	dnetesn	50649
                        40.	tosh	50647
                        41.	pjmlp	50620
                        42.	jonbaer	50451
                        43.	smacktoward	49551
                        44.	icebraining	47671
                        45.	coloneltcb	47628
                        46.	bane	46130
                        47.	wallflower	45600
                        48.	evo_9	45514
                        49.	nkurz	45305
                        50.	robin_reala	44759
                        51.	sp332	44413
                        52.	protomyth	43336
                        53.	wglb	43152
                        54.	walterbell	42181
                        55.	DanielBMarkham	42018
                        56.	untog	41473
                        57.	masklinn	41465
                        58.	userbinator	41398
                        59.	DiabloD3	40939
                        60.	petercooper	40624
                        61.	minimaxir	40221
                        62.	StavrosK	40031
                        63.	_delirium	39962
                        64.	signa11	39552
                        65.	btilly	39454
                        66.	zdw	38199
                        67.	grellas	37716
                        68.	bpierre	37253
                        69.	pavel_lishin	37120
                        70.	lisper	36755
                        71.	rdl	36589
                        72.	sethbannon	36380
                        73.	pcwalton	36356
                        74.	rdtsc	36352
                        75.	brudgers	35987
                        76.	stcredzero	35499
                        77.	toomuchtodo	35499
                        78.	pmoriarty	35443
                        79.	mpweiher	34665
                        80.	derefr	34356
                        81.	JoshTriplett	34267
                        82.	noonespecial	33911
                        83.	adventured	33881
                        84.	Garbage	33417
                        85.	jedberg	33101
                        86.	Retric	33100
                        87.	mtgx	33090
                        88.	sohkamyung	32766
                        89.	SwellJoe	32631
                        90.	Anon84	32493
                        91.	jonknee	32481
                        92.	cpeterso	32282
                        93.	wpietri	31987
                        94.	Someone1234	31715
                        95.	dredmorbius	31604
                        96.	scott_s	31496
                        97.	ilamont	30390
                        98.	nostromo	30147
                        99.	gruseom	30044
                        100.	philwelch	30032
                        '''
        # Debug code
        input_list = users_string.split()
        user_list = []
        # Generates indices from 0 on in intervals of 3
        user_indices = list(range(100))[0::3]
        for i in user_indices:
            user_list.append(input_list[i])
        
        return user_list
