#!/usr/bin/env python

import tweepy, praw, config, pprint,time

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)

api = tweepy.API(auth)

reddit = praw.Reddit(client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = config.user_agent)

hiphopheads = reddit.subreddit('hiphopheads')

print("---Hip Hop Heads Twitter Bot---")

posted = []
while True: 
	for submission in hiphopheads.new():
		if(submission.score > 20 and submission.id not in posted):
                        if(submission.author == 'AutoModerator'): continue
			print submission.score, submission.title 
			post = submission.title + " " + submission.url
			api.update_status(post)
			posted.append(submission.id)
	time.sleep(300)
