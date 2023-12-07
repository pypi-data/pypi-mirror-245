from redstat.variables.download import url

USER_URL_TYPES = {
    'all': url.USER_BASE_URL,
    'comment': url.USER_COMMENTS_URL,
    'post': url.USER_POSTS_URL
}

SUBREDDIT_URL_TYPES = {
    'all': url.SUBREDDIT_BASE_URL
}
