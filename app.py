import os, csv
from flask import Flask, request, redirect, url_for, render_template, session, send_file, make_response
from werkzeug.utils import secure_filename
from csv01 import makelistdict, getheareds
from mol02 import searchlistdict
from pprint import pprint
import sys


UPLOAD_FOLDER = './tmp/'
DOWNLOAD_FOLDER = './out/'
ALLOWED_EXTENSIONS = set(['txt','csv'])
PROCFILE = 'tmp.txt'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['PROC_FILE'] = PROCFILE
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

flist=''
filelist=os.listdir(app.config['UPLOAD_FOLDER'],)
if filelist != []:
    for file in filelist:
        flist = flist + "<a href='/proc/" + file + "'> " + file  + "</a><br>"
print(flist)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    reload(sys)
    sys.setdefaultencoding('utf8')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    flist = ''
    filelist = os.listdir(app.config['UPLOAD_FOLDER'], )
    if filelist != []:
        for file in filelist:
            flist = flist + "<a href='/proc/" + file + "'> " + file + "</a><br>"
    return """
    <!doctype html>
    <title>ButterflyNet Name Validation</title>
    <link rel=stylesheet type=text/css href="/static/bootstrap.min.css">
    <h1>ButterflyNet Name Validation</h1>
    <h3>Upload a .csv file and then select the file bellow to validate names</h3>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    <p>
    <p>
    <a href="/">Home</a>
    """ % flist
    #       % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

@app.route('/proc/<filename>')
def proc(filename):
    result=filename
    fname = app.config['UPLOAD_FOLDER']+ result
    if os.path.isfile(fname):
        result = makelistdict(fname, '', 'Genus', 'Species')
        print result
        dat = searchlistdict(result,18)
        session['res'] = dat
        headers = getheareds(fname)
        session['head'] = headers
        app.config['PROC_FILE'] = filename
        return render_template('form_action.html', results=dat)


@app.route('/save')
def save():
    results = session.get('res', None)
    headers = session.get('head', None)
    print (headers)
    fname = app.config['DOWNLOAD_FOLDER'] + app.config['PROC_FILE']
    columns = headers + (['Flag','user-supplied name','valid name'])
    print(columns)
    WriteDictToCSV(fname, columns, results)
    flist = ''
    filelist = os.listdir(app.config['DOWNLOAD_FOLDER'], )
    if filelist != []:
        for file in filelist:
            flist = flist + "<a href='./out/" + file + "' download> " + file + "</a><br>"
    print(os.path.isfile(fname))
    return """
    <!doctype html>
    <title>ButterflyNet Name Validation</title>
    <h1>ButterflyNet Name Validation</h1>
    <h2>.csv file saved.</h2>
    <p>%s</p>
    <p>
    <p>
    <a href="/">Home</a>
    """ % flist

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

@app.route("/out/<file_name>")
def getFile(file_name):
    headers = {"Content-Disposition": "attachment; filename=%s" % file_name}
    file_name = app.config['DOWNLOAD_FOLDER'] + file_name
    with open(file_name, 'r') as f:
        body = f.read()
    return make_response((body, headers))

if __name__ == "__main__":
    app.run(debug=True)

