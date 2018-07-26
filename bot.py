#!/usr/bin/env python

import logging
logging.basicConfig(filename='tweets.log', level=logging.INFO, format='%(asctime)s %(levelname)s : %(message)s')
import tweepy, praw, config, pprint, time, HTMLParser

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)

api = tweepy.API(auth)

reddit = praw.Reddit(client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = config.user_agent)

hiphopheads = reddit.subreddit('hiphopheads')

#logger = logging.getLogger('tweets')
#logger.setLevel(logging.INFO)

def main():
    print("---Hip Hop Heads Twitter Bot---")
    while True:
        query_reddit()
        time.sleep(300)

def get_last_tweets():
    tweets = []
    h = HTMLParser.HTMLParser()
    for status in api.user_timeline(tweet_mode='extended'):
        text = h.unescape(status.full_text).rsplit(' ', 1)[0]
        tweets.append(text)
    return tweets

def query_reddit(): 
    try:
        last_20_tweets = get_last_tweets();
        h = HTMLParser.HTMLParser()
        
        for submission in hiphopheads.new():
                if(((submission.score > 20 and "FRESH" in submission.title)
                    or (submission.score > 50)
                    or ("FRESH ALBUM" in submission.title))
                    and submission.author != 'AutoModerator'
                    and submission.title not in last_20_tweets
                    and "DISCUSSION" not in submission.title):

                        title = h.unescape(submission.title)
                        dif = (time.time() - submission.created_utc)/3600
                        log = str(submission.score) + " " + title + " " + str(dif)
                        print log
                        logging.info(log)

                        post = submission.title + " " + submission.url
                        api.update_status(post)
    except Exception as e:
        print e
        logging.warning(e)
        print last_20_tweets

if __name__ == '__main__':
    main()
