from flask import Flask, render_template, request, redirect, session, jsonify
import jinja2
import os
from secret import *
import json,httplib

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

def current_user_has_posted():
	if session.get('posted') is not None and session.get('posted') == POSTED_SECRET:
		return True
	return False

def change_user_to_posted():
	session['posted'] = POSTED_SECRET

def default_behavior(message=None):
	if not current_user_has_posted():
		return render_template('index.jade')
	if message is None:
		return render_template('index.jade', already_posted=True)
	# get message from parse
	return render_template('message.jade', message=message)

@app.route('/post_status', methods=['POST'])
def post_status():
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('POST', '/1/classes/Status', json.dumps({
   		"text": request.form.get("message")
 	}), {
   		"X-Parse-Application-Id": "HMKZdmKBHqOubVBDulljRW8gqhdueTnsqzLfVovc",
   		"X-Parse-REST-API-Key": "Tu0cErCkd0iZ2sj8PHf4ki50IkEAyfhOWTWhXIrW",
   		"Content-Type": "application/json"
 	})
	result = json.loads(connection.getresponse().read())
	return jsonify({"url": "localhost:8000/message/" + result.get('objectId')})

@app.route('/user_just_posted')
def just_posted():
	if request.args.get("message") is not None:
		change_user_to_posted()
		return redirect('/message/' + request.args.get("message"))
	return redirect('/')

@app.route('/', methods=['GET'])
def index():
	return default_behavior()

@app.route('/message/<message_id>')
def message(message_id):
	connection = httplib.HTTPSConnection('api.parse.com', 443)
	connection.connect()
	connection.request('GET', '/1/classes/Status/'+message_id, '', {
    	"X-Parse-Application-Id": "HMKZdmKBHqOubVBDulljRW8gqhdueTnsqzLfVovc",
       	"X-Parse-REST-API-Key": "Tu0cErCkd0iZ2sj8PHf4ki50IkEAyfhOWTWhXIrW"
    })
	result = json.loads(connection.getresponse().read())
	text=result.get("text")
	return default_behavior(text)

@app.route('/about')
def about():
	return render_template('about.jade')

@app.route('/share')
def share():
	return render_template('share.html')

# @app.route('/posted')
# def posted():
# 	change_user_to_posted()
# 	return redirect('/')

# @app.route('/not_posted')
# def not_posted():
# 	session.pop('posted', None)
# 	return redirect('/')

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)