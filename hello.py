from flask import Flask, render_template, jsonify
app = Flask(__name__)
#url_for('static', filename='style.css')

@app.route('/')
def hello_world():
	return render_template('twitMap.html')

@app.route('/twit')
def send_data():
	data = {'longitude':1.0,'latitude':1.0}
	return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
