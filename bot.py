#!/usr/bin/env python

import tweepy, praw, config, pprint, time, logging, HTMLParser

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)

api = tweepy.API(auth)

reddit = praw.Reddit(client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = config.user_agent)

hiphopheads = reddit.subreddit('hiphopheads')

logging.basicConfig(filename='out.log', level=logging.INFO)

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
        
        for submission in hiphopheads.new():
                if(((submission.score > 20 and "FRESH" in submission.title)
                    or (submission.score > 50)
                    or ("FRESH ALBUM" in submission.title))
                    and submission.author != 'AutoModerator'
                    and submission.title not in last_20_tweets
                    and "DISCUSSION" not in submission.title):

                        title = (submission.title).encode('ascii', 'ignore').decode('ascii')
                        log = str(submission.score) + " " + title
                        print log
                        logging.info(log)

                        post = submission.title + " " + submission.url
                        api.update_status(post) 
    except Exception as e:
        print e
        print last_20_tweets
        logging.warning(e)
        logging.warning(last_20_tweets)


if __name__ == '__main__':
    main()
