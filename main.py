from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2
print(cv2.__version__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png','webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'the random string'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def procImg(filename,operation):
    img= cv2.imread(f"uploads/{filename}")
    print(f"The operation is {operation} and the filename is {filename} ")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,imgProcessed)
            return newfilename
        case "cpng":
            # imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename= f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cwebp":
            # imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpg":
            # imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/doc')
def doc():
    return render_template("doc.html")

@app.route('/edit', methods=["GET","POST"])
def edit():
    if request.method == "POST":
        operation= request.form.get("opcode")
        if 'file' not in request.files:
            flash('No file part')
            return "ERROR: No File Selected"
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=procImg(filename,operation)
            flash(f"Your file is processed and available here <a href='/{new}' target='_blank'>{new}</a>")
            return render_template("index.html")
    
app.run(debug=True)
