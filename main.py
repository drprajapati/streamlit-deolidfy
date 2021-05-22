import os
from app import app
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template
import sys
import requests
import ssl
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file

from uuid import uuid4

from os import path
import torch

import fastai
from deoldify.visualize import *
from pathlib import Path

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
image_colorizer = get_image_colorizer(artistic=True)
print(image_colorizer)

if torch.cuda.is_available():
	torch.backends.cudnn.benchmark = True
	os.environ["CUDA_VISIBLE_DEVICES"] = "0"
else:
	del os.environ["CUDA_VISIBLE_DEVICES"]

	

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			process_image(filename)

		#else:
		#	flash('Allowed image types are -> png, jpg, jpeg, gif')
		#	return redirect(request.url)

	return render_template('upload.html', filenames=file_names)

def process_image(filename):
	result = image_colorizer.plot_transformed_image(path=Path('static/uploads/' + filename), results_dir=Path('static/results/'),figsize=(20,20), render_factor=20, display_render_factor=True, compare=False)
	return render_template('upload.html', filename=result)

@app.route('/display/<filename>', methods=['GET'])
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/results/<filename>',  methods=['GET'])
def results(filename):
	return redirect(url_for('static', filename='results/' + filename), code=301)

if __name__ == "__main__":
    
	app.run()