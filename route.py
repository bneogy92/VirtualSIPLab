from flask import Flask, render_template, request, make_response, send_from_directory
from werkzeug import secure_filename, datastructures
import os
from imProc.conEnh import Core
import re

app = Flask(__name__,static_url_path='/css')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'C:\Users\Ankur\Documents\GitHub\VirtualSIPLab\user_data'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = 'css'

@app.route('/css/<cssname>')
def send_css(cssname):
    print "in send_css"
    csspath=APP_ROOT+'\\css\\'
    print csspath
    return send_from_directory(csspath, cssname)

@app.route('/js/<jsname>')
def send_js(jsname):
    print "in send_js"
    jspath='\\js\\'+jsname
    return send_from_directory(APP_ROOT, jspath)

@app.route('/images/<imagename>')
def send_image(imagename):
    print "in send_images"
    imagepath=APP_ROOT+"\\images"
    print imagepath
    print imagename
    print imagepath+"\\"+imagename
    return send_from_directory(imagepath, imagename)


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/uploader', methods=['GET','POST'])
def uploader():
    print APP_ROOT
    print "i am in upload if"
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file_handle in files:
            if file_handle:
                print file_handle.filename
                fileExt=re.findall('[.]\S+', file_handle.filename)[0]
                print fileExt
                if fileExt=='.img':
                    fname=file_handle.filename #check by javascript that one file is hdr and one file is valid satellite image                    
                filename = secure_filename(file_handle.filename)
                fpath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print fpath
                file_handle.save(fpath)
        print "name",fname
        print "path",fpath
        return render_template('exp1.html',fname=fname)
    else:
        print "i am in upload else function"
        return render_template('upload.html')   

@app.route('/display/<fname>')
def display(fname):
    print "i am in display"
    fileExt=re.findall('[.]\S+', fname)[0]
    fpath=UPLOAD_FOLDER+"\\"+fname
    newName=fname
    if fileExt!='.jpg' and fileExt!='jpeg' and fileExt!='gif' and fileExt!='bmp':
        fname=Core.convert(UPLOAD_FOLDER,fname,newName,'jpg')
            
    return send_from_directory(UPLOAD_FOLDER, fname)

@app.route('/log/<fname>')
def log(fname):
    print "i am in log"
    path=UPLOAD_FOLDER+"\\"+fname
    print(path)
    newName=Core.Imagelog(path)
    return render_template('result.html',fname=newName)

@app.route('/experiments')
def experiments():
    return render_template('experiments.html')

if __name__ == '__main__':
   app.run(host='127.0.0.1',port=8000,debug = True)