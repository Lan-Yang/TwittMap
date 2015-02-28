import psycopg2

conn = psycopg2.connect(dbname='Twitter', user='postgres', password='postgres', host='127.0.0.1')
cur = conn.cursor()

cur.execute(r"INSERT INTO twit(t_longitude, t_latitude, t_content) VALUES (100,100,'great');")
conn.commit()
for record in cur:
	print record

cur.close()
conn.close()