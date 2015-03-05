import tweepy
import sys
import psycopg2
from flask import Flask, render_template, jsonify
application = app = Flask(__name__)

conn = psycopg2.connect(dbname='Twitter', user='postgres', password='postgres', host='twitmapdb.cgbzekjkgmas.us-east-1.rds.amazonaws.com')
cur = conn.cursor()

infile = open("keywords.txt","r")
words = [line.strip() for line in infile]
infile.close()

@app.route('/')
def hello_world():
	return render_template('twitMap.html',words=words)

@app.route('/twit/<keyword>')
def send_data(keyword):
	data = []
	sql = r"select t_longitude, t_latitude, t_content from twit order by t_id desc limit 500"
	cur.execute(sql)
	for line in cur:
		text = line[2].split()
		if keyword=='All':
			data.append({"latitude":line[1],"longitude":line[0]})
		else:
			if keyword in text:
				data.append({"latitude":line[1],"longitude":line[0]})
	return jsonify({"data":data})

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
