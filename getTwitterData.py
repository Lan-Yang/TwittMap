import tweepy
import sys
import psycopg2

conn = psycopg2.connect(dbname='Twitter', user='postgres', password='postgres', host='twitmapdb.cgbzekjkgmas.us-east-1.rds.amazonaws.com')
cur = conn.cursor()

infile = open("keys.txt","r")
keys = [line.strip() for line in infile]
infile.close()
infile = open("keywords.txt","r")
words = [line.strip() for line in infile]
infile.close()

consumer_key = keys[0]
consumer_secret = keys[1]
access_token = keys[2]
access_token_secret = keys[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

length = len(words)
keyword = words[0]

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.coordinates:
            text = status.text.encode('utf-8')
            text = text.replace("'","*")
            text = text.lower()
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            sql = r"INSERT INTO twit(t_longitude, t_latitude, t_content) VALUES (%s, %s, '%s')"%(longitude, latitude, text)
            cur.execute(sql)
            conn.commit() # Write SQL results to RDS

    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=[-130, -60, 70, 60])

