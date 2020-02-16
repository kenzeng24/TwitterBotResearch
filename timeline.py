"""
Author: Ken Zeng
Date: 16/02/2020
"""

import tweepy
import time
import csv
import json
from tweepy import TweepError
from tweepy import RateLimitError


def write_json(name,
               new_tweets,
               outfile):

    for tweet in new_tweets:
        # write each tweet json on a new line
        json.dump(tweet._json, outfile)
        outfile.write('\n')


def write_hashtags(name,
                   new_tweets,
                   outfile):

    writer = csv.writer(outfile)
    hashtags = []
    for tweet in new_tweets:
        for hashtag in tweet.entities.get('hashtags'):
            hashtags.append(hashtag["text"])
    writer.writerow([name, hashtags])


class TimelineCollector:
    """
    Collect data from a list of user's timeline
    using Twitter API and write the results into a file
    """
    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_key,
                 access_secret):
        try:
            # set up twitter API
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key,access_secret)
            self.api = tweepy.API(auth)
        except Exception as e:
            print(e)

    def write_users(self,
                    user_screen_names,
                    write_function,
                    filename,
                    print_failed=True,
                    print_unauthorized=True,
                    print_errors=True):

        unauthorized = []
        failed = []
        with open(filename, 'w') as outfile:
            for name in user_screen_names:
                timeout = True
                # timeout indicates that the rate is being limited
                while timeout:
                    try:
                        # write the most recent 200 tweets into a file using the write_function
                        new_tweets = self.api.user_timeline(screen_name=name, count=200)
                        write_function(name, new_tweets, outfile)
                        timeout = False
                    except RateLimitError as e:
                        # wait so rate limit can reset
                        time.sleep(20)
                    except TweepError as e:
                        if e.reason == 'Not authorized.':
                            unauthorized.append(name)
                        elif "Failed ot send request" in e.reason:
                            # Try again to see if internet gets better
                            pass
                        else:
                            failed.append(name)

                        if print_errors:
                            print(name, e)
                        timeout = False
        if print_failed:
            print(failed)

        if print_unauthorized:
            print(unauthorized)

    def collect_json(self,
                     user_screen_names,
                     filename):
        """
        collect the 200 most recent tweets of each user
        and save tweets as a txt file
        """
        self.write_users(user_screen_names, filename, write_json)

    def collect_hashtags(self,
                         user_screen_names,
                         filename):
        """
        collect the 200
        """
        self.write_users(user_screen_names, filename, write_hashtags)


if __name__ == "__main__":

    pass

