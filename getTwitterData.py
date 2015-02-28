import tweepy
import sys

consumer_key = 'd5qhU69TNYmuT608SPk7Wy5VZ'
consumer_secret = 'QuJziBDzwwss8P5WatwdZigCvhB5r2tphRbvWGOaKZ3RcY1cil'
access_token = '3019121609-3U2LQvT4XNYuWeX0SkSW7WdKhQlnF5JqP9lIemh'
access_token_secret = '3Q9jVLQaULyu2Kj0QEYgxzVvqURYZetTl1naOCi6ycxZl'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text.encode('utf-8')

    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=[-130, -60, 70, 60])