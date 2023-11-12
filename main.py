from analze import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('home.html', content='No file uploaded.')
        file = request.files['file']
        # Check if the file has a filename
        if file.filename == '':
            return render_template('home.html', content='No file selected.')
        filepath = 'email files/' + file.filename
        return render_template('home.html',
                               content=check_file_type(file),
                               features = get_features(filepath),
                               pre_content=predict_content(text_feature(filepath)),
                               pre_tag=predict_html(html_tags_feature(filepath)),
                               pre_num=predict_num(num_feature(filepath)),
                               pre_extra=predict_extra(extra_feature(filepath)))

    return render_template('home.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
