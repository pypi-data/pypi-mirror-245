BASE_URL = 'https://reddit.com/{}'

SUBREDDIT_BASE_URL = BASE_URL.format('r/{}.json')


USER_BASE_URL = BASE_URL.format('user/{}.json')
USER_POSTS_URL = USER_BASE_URL.format('{}/submitted')
USER_COMMENTS_URL = USER_BASE_URL.format('{}/comments')
