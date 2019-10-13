from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json

import twitter_credentials

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)



# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename, time_limit=15):
        self.start_time = time.time()
        self.limit = time_limit
        self.fetched_tweets_filename = fetched_tweets_filename
        super(StdOutListener, self).__init__()

    def on_data(self, raw_data):
        if (time.time() - self.start_time) < self.limit:
            try:
                with open(self.fetched_tweets_filename, 'a') as tf:
                    # parsing data
                    parsedRoute = json.loads(raw_data)
                    dataLocation = parsedRoute["user"]["location"]
                    if (dataLocation is not None):
                        print("New post with location found at: ", dataLocation)
                        newObj = {
                            "ml": {
                                "lang": parsedRoute["user"]["lang"],
                                "id": parsedRoute["user"]["id"],
                                "text": parsedRoute["text"]
                            },
                            "map": {
                                "locationText": dataLocation,
                            }
                        }
                        tf.write(jsonn.dump(newObj))
            except Exception as e:
                print("Error on_data %s" % str(e))
            return True
        else:
            return False

    def on_error(self, status):
        print(status)



if __name__ == '__main__':

    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["trump"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
