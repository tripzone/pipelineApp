import os
import json
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import functions
 
app = Flask(__name__)      
 
@app.route('/test')
def home():
   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = 'data.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global FYTech
            FYTech = functions.initiateDf()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/makeplot', methods=['GET'])
def make_plot():
    functions.generateTable(FYTech)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route('/makeplot2', methods=['GET'])
def make_plot2():
    functions.pipePlots(FYTech)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 




 
if __name__ == '__main__':
  app.run(debug=True)

