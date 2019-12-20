# Main application logic goes here
import hacker_access


top_users = hacker_access.get_user_list()

# Build top n users table
for username in top_users:

