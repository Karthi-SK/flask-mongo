from flask import Flask, render_template, request, Response
from pymongo import MongoClient
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)

client = MongoClient('mongodb://mongo:2URBet0GPFGwQNSGUkzO@containers-us-west-41.railway.app:7882')
db = client['covid-bot']
df = db.dialogflow

@app.route('/')
def index():
	result = df.find().sort('_id', -1)
	return render_template('index.html', result=result)

@app.route('/webhook', methods = ['POST', 'GET'])
def webhook():
	req = request.get_json(force = True)
	query = req['queryResult']['queryText']
	result = req['queryResult']['fulfillmentText']
	df.insert_one({'query': query, 'response': result})
	print('Data inserted successfully')
	return Response(status=200)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)