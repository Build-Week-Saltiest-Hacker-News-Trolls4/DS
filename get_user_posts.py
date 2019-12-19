import json
import requests


def get_user_posts(username, filter_posts="all", limit=100):
    """
    Filter by type of item. 
    One of "job", "story", "comment", "poll", or "pollopt"
    Default: type='comment', limit='100'
    """
    # TODO: currently only supports 'comment' type

    response = requests.get(f'https://hacker-news.firebaseio.com/v0/user/{username}.json')
    post_ids = response.json()["submitted"]
    
    filtered_post_ids = []
    filtered_posts = []
   
    for post_id in post_ids:
        
        # post is a python dict
        post = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{post_id}.json').json()

        if (post['type'] == filter_posts):
            
            text = post.get('text')   
            
            # text==null if post was deleted
            if text:
                filtered_posts.append(text)
                filtered_post_ids.append(post_id)
        
        # Checks whether the specified limit has been reached
        if len(filtered_posts) == limit:
            break

    return filtered_post_ids, filtered_posts
