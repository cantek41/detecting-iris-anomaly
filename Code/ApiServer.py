from flask import Flask, send_file
from PIL import Image
app = Flask(__name__)
@app.route("/")
def hello():
    return send_file("qrcode.png", mimetype="image/gif")
if __name__ == "__main__":    
    app.run(host="192.168.0.32")
