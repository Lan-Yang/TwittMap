import tweepy
import sys
import psycopg2

conn = psycopg2.connect(dbname='Twitter', user='postgres', password='postgres', host='127.0.0.1')
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
        	if keyword in text:
        		longitude = status.coordinates['coordinates'][0]
        		latitude = status.coordinates['coordinates'][1]
        		sql = r"INSERT INTO twit(t_longitude, t_latitude, t_content) VALUES (%s, %s, '%s')"%(longitude, latitude, text)
        		print sql
        	# Exclude special symbols in text
        		cur.execute(sql)
        		conn.commit()
            # print status.coordinates['coordinates'], status.text.encode('utf-8')

    def on_error(self, status_code):
        print >> sys.stderr, 'Error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=[-130, -60, 70, 60])
