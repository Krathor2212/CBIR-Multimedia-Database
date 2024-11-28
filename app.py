from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import search_similar_images, add_image_to_db
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)
    add_image_to_db(file.filename, image_path, "Uploaded image-Gallery")

    results = search_similar_images(image_path)
    results = [dict(t) for t in {tuple(d.items()) for d in results}]

    print(len(results))
    print("Results:", results)
    
    return render_template('results.html', results=results)

@app.route('/previous-uploads')
def previous_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return render_template('previous_uploads.html', files=files)

@app.route('/api/previous-uploads', methods=['GET'])
def api_previous_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)
