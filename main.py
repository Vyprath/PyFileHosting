from flask import Flask, render_template, request, url_for
from random import sample
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/mnt/ofc.wlpizza_storage"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max 100 MB.
ALLOWED_EXTENSIONS = [
    'js', 'css', 'html', 'json', 'txt', 'mp4', 'avi', 'flv', 'mov', 'wmv',
    'png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp', 'mp3', 'wav', 'flac', 'aac',
    'ogg', 'alac', 'zip', '7z', 'rar', 'pdf', 'exe']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', allowed_ext=", ".join(ALLOWED_EXTENSIONS))


@app.route('/upload', methods=['POST'])
def upload():
    fileob = request.files["file"]
    fext = secure_filename(fileob.filename).split('.')[-1].lower()
    if fext.lower() not in ALLOWED_EXTENSIONS:
        return "Error: Filename extension not allowed."
    filename = "{}.{}".format(''.join(sample(string.ascii_letters + string.digits, 6)), fext)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    return '/files/' + filename
