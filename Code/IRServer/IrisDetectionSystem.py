from flask import Flask
from flask import  request, redirect, url_for, jsonify
import os
import label_image

import hashlib

app = Flask(__name__)
list=[]
@app.route('/login')
def login():
    hash_object=hashlib.md5(request.remote_addr.encode("utf-8"))
    id=hash_object.hexdigest()
    if id not in list:
        list.append(id)
    return id

    
@app.route('/takeImage', methods=['POST'])
def takeImage():
    hash_object=haslib.md5(request.remote_addr.encode("utf-8"))
    id=hash_object.hexdigest()
    if id not in list:
        return redirect(request.url),404
    if request.method == 'POST':
        # check if the post request has the file part
        print("dfed")
        if 'file' not in request.files:
            print("No file part")# flash('No file part')
            return redirect(request.url)
        print(request.files)
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            print("No 564 file part")
            return redirect(request.url)
        file.save(os.path.join("", file.filename))
        res=label_image.classify(file.filename)
    return jsonify(res)

if __name__ == "__main__":    
    app.run("192.168.0.34")
