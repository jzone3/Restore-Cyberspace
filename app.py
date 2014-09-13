from flask import Flask, render_template, request, redirect, session
import jinja2
import os
from secret import *

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

def current_user_has_posted():
	if session.get('posted') is not None and session.get('posted') == POSTED_SECRET:
		return True
	return False

def change_user_to_posted():
	session['posted'] = POSTED_SECRET

def default_behavior(message_id=None):
	if not current_user_has_posted():
		return render_template('index.jade')
	if message_id is None:
		return render_template('index.jade', already_posted=True)
	# get message from parse
	return render_template('message.jade', message=message_id)

@app.route('/')
def index():
	return default_behavior()

@app.route('/message/<message_id>')
def message(message_id):
	return default_behavior(message_id)

@app.route('/about')
def about():
	return render_template('about.jade')

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