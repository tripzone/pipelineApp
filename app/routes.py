import os
import json
from flask import Flask, request, redirect, jsonify
import functions as fn
from flask_cors import CORS

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route('/test')
def home():
   return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['xlsx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			print('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			print('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			# filename = secure_filename(file.filename)
			filename = 'data.xlsx'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			FY = fn.initiateDf()
			fn.initiateTech(FY)
			return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/makeplot', methods=['GET'])
def make_plot():
	type = request.headers.get('plot-type')
	if len(list(filter(lambda x : x['type'] == type, fn.plots))) > 0:
		try:
			fn.plotIt(type)
			return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
		except Exception as e:
			return json.dumps({'success':False, 'error':'No file uploaded '+str(e)}), 200, {'ContentType':'application/json'}
	else:
		return json.dumps({'success':False, 'error':'Invalid plot type: '+type}), 200, {'ContentType':'application/json'}

@app.route('/plottypes', methods=['GET'])
def plot_types():
	plotsCopy = fn.plots
	a = list(map(lambda x: {"type":x['type'], "category":x['category'], "desc":x['desc']}, fn.plots))
	print(a)
	return jsonify(a), 200, {'ContentType':'application/json'}

# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        return "no good bro"


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)
