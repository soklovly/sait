from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from collections import Counter
import re

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'

def count_words(file_path):
    words = re.findall(r'\w+', open(file_path, 'r', encoding='utf-8').read().lower())
    word_counts = Counter(words)
    sorted_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts

@app.route('/', methods=['GET', 'POST'])
def home():
    txt_file_error = False
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            file.save(secure_filename(file.filename))
            word_counts = count_words(file.filename)
            return render_template('res.html', word_counts=word_counts)
        else:
            txt_file_error = True
    return render_template('home.html', txt_file_error=txt_file_error)

@app.route('/index')
def about():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
